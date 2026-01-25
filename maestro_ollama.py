import os
import json
import time
import re
import pandas as pd
import requests

# --- 1. CONFIGURAÇÃO DO OLLAMA ---
# Se rodar no Lenovo: use 'http://localhost:11434'
# Se rodar no Desktop (acessando pelo Lenovo): use 'http://IP_DO_DESKTOP:11434'
OLLAMA_URL = "http://localhost:11434/api/generate"

# ESCOLHA SEU MODELO AQUI (Comente/Descomente conforme o hardware)
# MODEL_NAME = "phi3.5"           # Ultra-leve (Lenovo - Rápido, menos criativo)
# MODEL_NAME = "qwen2.5:7b"       # Equilibrado (Lenovo - Recomendado)
MODEL_NAME = "mistral-nemo:12b" # Alta Qualidade (Desktop/Ryzen - Maestro Class)

# --- 2. CONSTANTES E HACKS DO SUNO ---
MAX_LYRIC_CHARS = 4000
MAX_STYLE_CHARS = 900
MAX_MODE_HEADER = """[Is_MAX_MODE: MAX](MAX)
[QUALITY: MAX](MAX)
[REALISM: MAX](MAX)
[REAL_INSTRUMENTS: MAX](MAX)"""

# --- 3. CARREGAMENTO DE INTELIGÊNCIA (JSONs da pasta data/) ---
def load_maestro_data(genre, gender):
    """
    Carrega dados inteligentes dos arquivos JSON para enriquecer o prompt.
    Retorna contexto formatado para injeção no prompt do LLM.
    """
    context_data = ""
    
    # A. Carregar Perfil Vocal
    try:
        vocal_path = 'vocal_profiles.json'
        if os.path.exists('data/vocal_profiles.json'):
            vocal_path = 'data/vocal_profiles.json'
            
        with open(vocal_path, 'r', encoding='utf-8') as f:
            vocal_db = json.load(f)
            profiles = vocal_db['vocal_characteristics_guide']['profiles']
            
            # Busca case-insensitive
            target_profile = None
            for key in profiles.keys():
                if key.lower() == genre.lower():
                    target_profile = profiles[key]
                    break
            
            if target_profile:
                gender_key = 'female' if 'fem' in gender.lower() else 'male'
                specs = target_profile.get(gender_key, target_profile.get('male', {}))
                context_data += f"\n[VOCAL PROFILE]: {specs.get('description', 'N/A')}\n"
                context_data += f"[MANDATORY VOCAL TAGS]: {specs.get('suno_tags', 'N/A')}\n"
            else:
                context_data += f"\n[VOCAL PROFILE]: Generic {gender} vocals for {genre}.\n"
    except Exception as e:
        context_data += f"\n[WARNING]: Could not load vocal profiles. ({e})\n"

    # B. Carregar Conhecimento Sonoro (Audio Specs & Fusions)
    try:
        knowledge_path = 'maestro_knowledge.json'
        if os.path.exists('data/maestro_knowledge.json'):
            knowledge_path = 'data/maestro_knowledge.json'
            
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            audio_db = json.load(f)
            
            # Receitas de fusão de gêneros
            fusions = audio_db.get('genre_fusion_recipes', {})
            for fusion_key in fusions.keys():
                if fusion_key.lower() in genre.lower() or genre.lower() in fusion_key.lower():
                    context_data += f"\n[GENRE RECIPE]: {fusions[fusion_key]}\n"
                    break
            
            # Características sônicas disponíveis
            sonic_chars = audio_db.get('sonic_characteristics', {})
            if sonic_chars:
                sonic_keys = ", ".join(sonic_chars.keys())
                context_data += f"\n[AVAILABLE SONIC TEXTURES]: {sonic_keys}\n"
                context_data += "[INSTRUCTION]: Select 1-2 textures that fit the aesthetic.\n"
            
    except Exception as e:
        # Falha silenciosa - não crítico
        pass

    return context_data

# --- 4. SYSTEM PROMPT (MAESTRO AI - Enhanced with Context Injection) ---
def get_ollama_prompt(tema, estetica_usuario, maestro_context):
    return f"""
    ROLE: You are MAESTRO AI, the ultimate audio architect for Suno v5.
    You have access to a comprehensive database of vocal profiles, sonic textures, and genre fusion recipes.
    
    INPUT:
    - Theme/Concept: "{tema}"
    - Aesthetic Goal: "{estetica_usuario}"
    
    DATABASE CONTEXT:
    {maestro_context}
    
    STRICT RULES (Do not disobey):
    1. STYLE PROMPT:
       - Limit: {MAX_STYLE_CHARS} chars.
       - Format: [BPM] BPM; [Instrumentation]; [Production tags]; [Vocal Tags].
       - MUST include the [MANDATORY VOCAL TAGS] provided above.
       - Select 1-2 textures from [AVAILABLE SONIC TEXTURES] if applicable.
       - Use technical terms from audio engineering (e.g., "tape saturation", "wide stereo", "sidechain").
       - If a [GENRE RECIPE] is provided, incorporate its elements.
    
    2. LYRICS:
       - Limit: {MAX_LYRIC_CHARS} chars.
       - Structure: [Intro], [Verse 1], [Chorus], [Verse 2], [Bridge], [Outro].
       - Language: English.
       - Header: The lyrics MUST start with the tag [START_ON: TRUE].
       - Content: Use the "Socratic" method - deep, meaningful lyrics, avoiding clichés.
       - Show, don't tell. Use metaphors and imagery.

    OUTPUT FORMAT:
    You must output VALID JSON only. Do not add markdown blocks like ```json.
    {{
        "title": "Song Title",
        "style_prompt": "The technical style string",
        "lyrics": "The full lyrics with tags"
    }}
    """

# --- 5. FUNÇÃO DE GERAÇÃO (REQUEST HTTP) ---
def clean_json_response(text):
    """Limpa markdown que LLMs locais adoram colocar (```json ... ```)"""
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*$', '', text)
    return text.strip()

def gerar_lote_ollama(csv_path):
    print(f"\n🎹 MAESTRO AI (Local): Initializing with model {MODEL_NAME}...")
    print("🖥️  GPU Optimization: Enabled for RTX 4070 Super")
    
    # Cria CSV de exemplo se necessário
    if not os.path.exists(csv_path):
        pd.DataFrame({
            'album': ['Example Album', 'Example Album'],
            'tema': ['The Ghost in the Machine', 'Digital Purgatory'],
            'estetica': ['Persona: JOHN WEISS (Grunge/Industrial)', 'Persona: NEON SERAPH-01 (Hyperpop)'],
            'processada': ['nao', 'nao'],
            'observacoes': ['', ''],
            'genre': ['Industrial', 'Hyperpop'],
            'gender': ['male', 'female']
        }).to_csv(csv_path, index=False)
        print("Created example CSV.")
        return []

    # Lê o CSV com as novas colunas
    df = pd.read_csv(csv_path)
    
    # Validação de colunas obrigatórias
    required_cols = ['album', 'tema', 'estetica', 'processada']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"❌ ERRO: Colunas faltando no CSV: {missing_cols}")
        print("   Adicione as colunas: album, tema, estetica, processada, observacoes")
        return []
    
    # Filtra apenas músicas não processadas
    df_pendentes = df[df['processada'].str.lower() != 'sim'].copy()
    
    if df_pendentes.empty:
        print("✅ Todas as músicas já foram processadas!")
        return []
    
    print(f"\n📊 Status: {len(df_pendentes)} músicas pendentes de {len(df)} totais")
    
    # Agrupa por álbum para manter consistência temática
    albums = df_pendentes['album'].unique()
    print(f"📀 Álbuns na fila: {', '.join(albums)}\n")
    
    lote_pronto = []

    for album in albums:
        tracks_album = df_pendentes[df_pendentes['album'] == album]
        print(f"\n🎸 === PROCESSANDO ÁLBUM: {album} ({len(tracks_album)} faixas) ===")
        
        for idx, row in tracks_album.iterrows():
            print(f"   ➤ Compondo: [{row['album']}] - {row['tema']}...")
            
            # Carrega contexto inteligente dos JSONs
            maestro_context = load_maestro_data(
                str(row.get('genre', 'Rock')), 
                str(row.get('gender', 'male'))
            )
            
            # Adiciona contexto do álbum ao prompt
            prompt = get_ollama_prompt(
                f"Album: {row['album']} | Track: {row['tema']}", 
                row['estetica'], 
                maestro_context
            )

            payload = {
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0.9,     # Alta criatividade
                    "num_ctx": 8192,        # Contexto massivo (sua RAM suporta)
                    "num_gpu": 99,          # Força uso da GPU
                    "num_thread": 8         # Otimiza para CPU de 8 threads
                }
            }

            try:
                start_time = time.time()
                response = requests.post(OLLAMA_URL, json=payload, timeout=180)
                response.raise_for_status()
                
                # Parsing
                result_json = response.json()
                raw_text = clean_json_response(result_json['response'])
                data = json.loads(raw_text)
                
                # Pós-processamento (Injeção de Headers MAX MODE)
                style_clean = data.get('style_prompt', '').replace(MAX_MODE_HEADER, "").strip()
                final_style = f"{MAX_MODE_HEADER}\n{style_clean}"
                if len(final_style) > MAX_STYLE_CHARS:
                    final_style = final_style[:MAX_STYLE_CHARS]
                
                lyrics_clean = data.get('lyrics', '').replace(MAX_MODE_HEADER, "").replace("[START_ON: TRUE]", "").strip()
                final_lyrics = f"{MAX_MODE_HEADER}\n\n[START_ON: TRUE]\n\n{lyrics_clean}"

                track = {
                    "id": idx,
                    "album": row['album'],
                    "title": data.get('title', 'Untitled'),
                    "original_tema": row['tema'],
                    "style_prompt": final_style,
                    "lyrics": final_lyrics,
                    "status": "ready"
                }
                lote_pronto.append(track)
                
                # Marca como processada no DataFrame
                df.at[idx, 'processada'] = 'sim'
                df.at[idx, 'observacoes'] = f"Processada em {time.strftime('%Y-%m-%d %H:%M:%S')}"
                
                # Salva backup incremental do JSON
                with open('suno_batch.json', 'w', encoding='utf-8') as f:
                    json.dump(lote_pronto, f, ensure_ascii=False, indent=2)
                
                # Atualiza o CSV após cada música processada
                df.to_csv(csv_path, index=False)
                
                duration = time.time() - start_time
                print(f"      ✅ Sucesso em {duration:.2f}s! Marcada como processada.")

            except requests.exceptions.Timeout:
                print(f"      ❌ Timeout: Modelo demorou mais de 180s")
                df.at[idx, 'observacoes'] = f"ERRO: Timeout em {time.strftime('%Y-%m-%d %H:%M:%S')}"
                df.to_csv(csv_path, index=False)
            except Exception as e:
                print(f"      ❌ Erro: {e}")
                df.at[idx, 'observacoes'] = f"ERRO: {str(e)[:100]}"
                df.to_csv(csv_path, index=False)

    # Salva CSV final atualizado
    df.to_csv(csv_path, index=False)
    print(f"\n✅ Processamento concluído! {len(lote_pronto)} músicas geradas.")
    print(f"📁 Resultados salvos em: suno_batch.json")
    print(f"📝 CSV atualizado: {csv_path}")
    print(f"\n✨ Execute 'maestro_brave_automator.py' para injetar no Suno.")
    
    return lote_pronto

if __name__ == "__main__":
    gerar_lote_ollama('fila_suno.csv')