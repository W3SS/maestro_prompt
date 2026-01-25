import os
import json
import time
import re
import pandas as pd
import requests

# --- 1. CONFIGURAÇÃO DO OLLAMA ---
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral-nemo:12b"  # Alta Qualidade (Desktop/Ryzen - Maestro Class)

# --- 2. CONSTANTES E HACKS DO SUNO ---
MAX_LYRIC_CHARS = 4000
MAX_STYLE_CHARS = 900
MAX_MODE_HEADER = """[Is_MAX_MODE: MAX](MAX)
[QUALITY: MAX](MAX)
[REALISM: MAX](MAX)
[REAL_INSTRUMENTS: MAX](MAX)"""

# --- 3. CARREGADOR INTELIGENTE DE DADOS (TODOS OS ARQUIVOS JSON) ---
class MaestroDataLoader:
    """Carrega e gerencia todos os arquivos de dados da pasta data/"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.vocal_profiles = self._load_json('vocal_profiles.json')
        self.audio_specs = self._load_json('audio_specs.json')
        self.genre_fusion = self._load_json('genre_fusion_matrix.json')
        self.instruments = self._load_json('instrument_specs.json')
        self.harmonic_progressions = self._load_json('harmonic_progressions.json')
        self.scales_emotions = self._load_json('scales_emotions.json')
        self.style_correlation = self._load_json('style_correlation.json')
        self.maestro_knowledge = self._load_json('maestro_knowledge.json')
        # New enhanced data files
        self.aesthetics_semiotics = self._load_json('aesthetics_semiotics.json')
        self.mood_psychoacoustics = self._load_json('mood_psychoacoustics.json')

    
    def _load_json(self, filename):
        """Carrega JSON da pasta data/ ou raiz como fallback, priorizando versões enhanced"""
        try:
            # Tenta carregar versão enhanced primeiro
            base_name = filename.replace('.json', '')
            enhanced_filename = f"{base_name}_enhanced.json"
            
            # Tenta enhanced na pasta data/
            enhanced_path = os.path.join(self.data_dir, enhanced_filename)
            if os.path.exists(enhanced_path):
                print(f"✅ Loading enhanced: {enhanced_filename}")
                with open(enhanced_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Tenta versão normal na pasta data/
            path = os.path.join(self.data_dir, filename)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Fallback para raiz (enhanced)
            if os.path.exists(enhanced_filename):
                print(f"✅ Loading enhanced from root: {enhanced_filename}")
                with open(enhanced_filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Fallback para raiz (normal)
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return {}
        except Exception as e:
            print(f"⚠️  Warning: Could not load {filename}: {e}")
            return {}
    
    def get_vocal_profile(self, genre, gender):
        """Retorna perfil vocal detalhado com referências de artistas"""
        try:
            profiles = self.vocal_profiles.get('vocal_characteristics_guide', {}).get('profiles', {})
            
            # Busca case-insensitive
            target_profile = None
            for key in profiles.keys():
                if key.lower() == genre.lower():
                    target_profile = profiles[key]
                    break
            
            if target_profile:
                gender_key = 'female' if 'fem' in gender.lower() else 'male'
                specs = target_profile.get(gender_key, target_profile.get('male', {}))
                
                return {
                    'artist_reference': specs.get('artist_reference', 'N/A'),
                    'description': specs.get('description', 'N/A'),
                    'suno_tags': specs.get('suno_tags', 'N/A')
                }
            return None
        except:
            return None
    
    def get_sonic_characteristics(self, aesthetic_keywords):
        """Retorna características sônicas baseadas em palavras-chave da estética"""
        try:
            sonic_chars = self.audio_specs.get('sonic_characteristics', {})
            matched_chars = []
            
            # Busca por palavras-chave na estética
            aesthetic_lower = aesthetic_keywords.lower()
            for char_name, char_desc in sonic_chars.items():
                if char_name in aesthetic_lower or any(word in aesthetic_lower for word in char_name.split('_')):
                    matched_chars.append(f"{char_name}: {char_desc}")
            
            # Se não encontrou nada, retorna algumas características genéricas
            if not matched_chars and sonic_chars:
                # Pega 3 características aleatórias relevantes
                import random
                available = list(sonic_chars.items())[:10]
                matched_chars = [f"{k}: {v}" for k, v in random.sample(available, min(3, len(available)))]
            
            return matched_chars
        except:
            return []
    
    def get_genre_fusion_recipe(self, genre):
        """Retorna receita de fusão de gênero se disponível"""
        try:
            recipes = self.genre_fusion.get('genres', {}).get('fusion_recipes', [])
            
            for recipe in recipes:
                if genre.lower() in recipe.get('name', '').lower():
                    return {
                        'name': recipe.get('name'),
                        'formula': recipe.get('formula'),
                        'key_elements': recipe.get('key_elements')
                    }
            return None
        except:
            return None
    
    def get_instrumentation(self, genre):
        """Retorna instrumentação específica do gênero"""
        try:
            mainstream = self.instruments.get('instrumentation_map', {}).get('mainstream_clusters', {})
            niche = self.instruments.get('instrumentation_map', {}).get('niche_clusters', {})
            fusion = self.instruments.get('instrumentation_map', {}).get('fusion_recipes', {})
            
            # Busca em todas as categorias
            for cluster in [mainstream, niche, fusion]:
                for key, value in cluster.items():
                    if key.lower() == genre.lower() or genre.lower() in key.lower():
                        return value
            return None
        except:
            return None
    
    def get_harmonic_context(self, theme_keywords):
        """Retorna contexto harmônico baseado no tema"""
        try:
            if not self.harmonic_progressions:
                return None
            
            # Analisa o tema para sugerir progressões
            theme_lower = theme_keywords.lower()
            suggestions = []
            
            # Busca por emoções/temas específicos
            if any(word in theme_lower for word in ['dark', 'sad', 'melancholic', 'doom', 'death']):
                suggestions.append("Minor key progressions, diminished chords, dark atmosphere")
            elif any(word in theme_lower for word in ['happy', 'uplifting', 'joy', 'celebration']):
                suggestions.append("Major key progressions, bright chords, uplifting atmosphere")
            elif any(word in theme_lower for word in ['epic', 'cinematic', 'grand', 'massive']):
                suggestions.append("Orchestral progressions, wide intervals, dramatic builds")
            
            return suggestions if suggestions else None
        except:
            return None
    
    def get_scale_emotion_mapping(self, theme, genre, bpm_hint=None):
        """Retorna mapeamento detalhado de escalas para emoções com artistas e progressões"""
        try:
            # Tenta carregar versão enhanced primeiro
            scales_data = None
            if os.path.exists('data/scales_emotions_enhanced.json'):
                with open('data/scales_emotions_enhanced.json', 'r', encoding='utf-8') as f:
                    scales_data = json.load(f)
            elif self.scales_emotions:
                scales_data = self.scales_emotions
            
            if not scales_data or 'scales_database' not in scales_data:
                return None
            
            # Analisa o tema para sugerir escalas
            theme_lower = theme.lower()
            genre_lower = genre.lower()
            scale_suggestions = []
            
            # Mapeamento de emoções/temas para escalas (expandido)
            emotion_keywords = {
                'dark': ['phrygian', 'locrian', 'harmonic_minor', 'phrygian_dominant'],
                'evil': ['phrygian', 'locrian', 'phrygian_dominant', 'super_locrian'],
                'mysterious': ['whole_tone', 'lydian_dominant', 'melodic_minor', 'enigmatic'],
                'sad': ['minor_aeolian', 'dorian', 'phrygian'],
                'aggressive': ['phrygian_dominant', 'super_locrian', 'phrygian_natural_3'],
                'peaceful': ['lydian', 'major_ionian', 'major_pentatonic'],
                'exotic': ['phrygian_dominant', 'hungarian_minor', 'hirajoshi', 'persian_major'],
                'spiritual': ['mixolydian', 'dorian', 'in_sen'],
                'epic': ['phrygian_dominant', 'harmonic_major', 'harmonic_minor'],
                'chaotic': ['locrian', 'super_locrian', 'octatonic_half_whole'],
                'groovy': ['dorian', 'mixolydian', 'mixolydian_b6'],
                'technical': ['super_locrian', 'altered_dominant', 'octatonic_half_whole']
            }
            
            # Busca por emoções no tema
            matched_scales = set()
            for emotion, scale_ids in emotion_keywords.items():
                if emotion in theme_lower:
                    matched_scales.update(scale_ids)
            
            # Busca por gênero específico
            genre_scale_map = {
                'djent': ['phrygian', 'lydian', 'mixolydian_b6', 'octatonic_half_whole'],
                'death': ['phrygian', 'phrygian_dominant', 'harmonic_minor', 'locrian'],
                'doom': ['minor_aeolian', 'blues_scale', 'minor_pentatonic', 'phrygian'],
                'thrash': ['phrygian', 'minor_aeolian', 'harmonic_minor'],
                'black': ['phrygian', 'locrian', 'harmonic_minor'],
                'prog': ['lydian', 'dorian', 'melodic_minor', 'lydian_dominant'],
                'tech': ['super_locrian', 'altered_dominant', 'octatonic_half_whole']
            }
            
            for genre_key, scale_ids in genre_scale_map.items():
                if genre_key in genre_lower:
                    matched_scales.update(scale_ids)
            
            # Se não encontrou nada, usa escalas padrão baseadas no gênero
            if not matched_scales:
                if 'metal' in genre_lower:
                    matched_scales = {'phrygian', 'minor_aeolian', 'harmonic_minor'}
                else:
                    matched_scales = {'major_ionian', 'minor_aeolian'}
            
            # Busca detalhes das escalas matched
            for scale in scales_data['scales_database']:
                if scale['id'] in matched_scales:
                    suggestion = f"**{scale['name']}**"
                    
                    # Adiciona mood
                    if 'psychoacoustics' in scale:
                        suggestion += f" → {scale['psychoacoustics']['primary_mood']}"
                    
                    # Adiciona artistas de referência
                    if 'artist_references' in scale and scale['artist_references']:
                        artists = ', '.join(scale['artist_references'][:2])  # Limita a 2
                        suggestion += f" (Artists: {artists})"
                    
                    # Adiciona progressões características
                    if 'signature_chords' in scale and scale['signature_chords']:
                        chords = scale['signature_chords'][0]  # Pega a primeira
                        suggestion += f" | Chords: {chords}"
                    
                    # Adiciona BPM range se disponível
                    if 'bpm_range' in scale and bpm_hint:
                        bpm_min, bpm_max = scale['bpm_range']
                        if bpm_min <= bpm_hint <= bpm_max:
                            suggestion += f" | BPM: {bpm_min}-{bpm_max} ✓"
                    
                    # Adiciona dificuldade
                    if 'difficulty' in scale:
                        suggestion += f" | Difficulty: {scale['difficulty']}"
                    
                    scale_suggestions.append(suggestion)
            
            return scale_suggestions[:3] if scale_suggestions else None  # Limita a 3
        except Exception as e:
            print(f"⚠️  Warning in get_scale_emotion_mapping: {e}")
            return None
    
    def get_aesthetic_context(self, estetica_text):
        """Retorna contexto semiótico rico baseado em arquétipos de cultura pop"""
        try:
            archetypes = self.aesthetics_semiotics.get('pop_culture_archetypes', {})
            matched_archetype = None
            estetica_lower = estetica_text.lower()
            
            for arc_id, arc_data in archetypes.items():
                if arc_id.replace('_', ' ') in estetica_lower or arc_id in estetica_lower:
                    matched_archetype = arc_data
                    break
            
            if matched_archetype:
                lines = [f"\n[AESTHETIC ARCHETYPE - {arc_id.replace('_', ' ').title()}]"]
                lines.append(f"Directorial Tone: {matched_archetype['directorial_tone']}")
                lines.append(f"Visual Mood: {matched_archetype['visual_mood']}")
                lines.append(f"Semiotic Signifiers: {', '.join(matched_archetype['semiotic_signifiers'])}")
                lines.append(f"Audio Synesthesia: {', '.join(matched_archetype['audio_synesthesia'])}")
                lines.append(f"Dynamics Profile: {matched_archetype['dynamics_profile']}")
                return "\n".join(lines)
            return None
        except Exception:
            return None

    def get_mood_context(self, mood_name):
        """Retorna contexto psicoacústico baseado no mood solicitado"""
        try:
            moods = self.mood_psychoacoustics.get('emotional_states', {})
            matched_mood = None
            mood_lower = mood_name.lower() if mood_name else ""
            
            for m_id, m_data in moods.items():
                if m_id in mood_lower:
                    matched_mood = m_data
                    break
            
            if matched_mood:
                lines = [f"\n[MOOD & PSYCHOACOUSTICS - {m_id.upper()}]"]
                lines.append(f"Description: {matched_mood['description']}")
                lines.append(f"Suggested Key: {', '.join(matched_mood['key_preference'])}")
                lines.append(f"BPM Range: {matched_mood['bpm_range']}")
                targets = matched_mood['psychoacoustic_targets']
                lines.append(f"Phsycoacoustic Focus: {targets['frequency_focus']}")
                lines.append(f"Dynamics Strategy: {targets['dynamics']}")
                lines.append(f"Spatial Imaging: {targets['spatial']}")
                return "\n".join(lines)
            return None
        except Exception:
            return None

    def build_context(self, tema, estetica, genre, gender, mood=None):
        """Constrói contexto completo integrando todos os dados"""
        context_parts = []
        
        # 1. Perfil Vocal
        vocal = self.get_vocal_profile(genre, gender)
        if vocal:
            context_parts.append(f"\n[VOCAL PROFILE - {vocal['artist_reference']}]")
            context_parts.append(f"Description: {vocal['description']}")
            context_parts.append(f"MANDATORY TAGS: {vocal['suno_tags']}")
        
        # 2. Receita de Fusão de Gênero
        fusion = self.get_genre_fusion_recipe(genre)
        if fusion:
            context_parts.append(f"\n[GENRE FUSION RECIPE - {fusion['name']}]")
            context_parts.append(f"Formula: {fusion['formula']}")
            context_parts.append(f"Key Elements: {fusion['key_elements']}")
        
        # 3. Instrumentação
        instruments = self.get_instrumentation(genre)
        if instruments:
            context_parts.append(f"\n[INSTRUMENTATION]")
            context_parts.append(f"{instruments}")
        
        # 4. Semiótica e Estética (Pop Culture Archetypes)
        aesthetic_context = self.get_aesthetic_context(estetica)
        if aesthetic_context:
            context_parts.append(aesthetic_context)
        
        # 5. Mood e Psicoacústica
        mood_context = self.get_mood_context(mood)
        if mood_context:
            context_parts.append(mood_context)

        # 6. Características Sônicas (Baseado em audio_specs.json)
        sonic = self.get_sonic_characteristics(estetica)
        if sonic:
            context_parts.append(f"\n[SONIC CHARACTERISTICS]")
            for char in sonic[:3]:  # Limita a 3 para não sobrecarregar
                context_parts.append(f"- {char}")
        
        # 7. Contexto Harmônico
        harmonic = self.get_harmonic_context(tema)
        if harmonic:
            context_parts.append(f"\n[HARMONIC SUGGESTIONS]")
            for suggestion in harmonic:
                context_parts.append(f"- {suggestion}")
        
        # 8. Escalas e Emoções (Enhanced)
        scales = self.get_scale_emotion_mapping(tema, genre)
        if scales:
            context_parts.append(f"\n[SCALE/EMOTION MAPPING - Enhanced]")
            for scale in scales:
                context_parts.append(f"- {scale}")
        
        return "\n".join(context_parts)


# --- 4. SYSTEM PROMPT (MAESTRO AI - Enhanced) ---
def get_ollama_prompt(tema, estetica_usuario, maestro_context):
    return f"""
    ROLE: You are MAESTRO AI, the ultimate audio architect for Suno v5.
    You have access to a comprehensive database of vocal profiles, sonic textures, genre fusion recipes,
    instrumentation specs, harmonic progressions, and scale/emotion mappings.
    
    INPUT:
    - Theme/Source of Inspiration: "{tema}"
    - Aesthetic Archetype/Expression: "{estetica_usuario}"
    
    COMPREHENSIVE DATABASE CONTEXT:
    {maestro_context}
    
    STRICT RULES (Do not disobey):
    1. STYLE PROMPT ({MAX_STYLE_CHARS} chars max):
       - Format: [BPM] BPM; [Instrumentation from DATABASE]; [Sonic Characteristics]; [MANDATORY VOCAL TAGS].
       - MUST include the MANDATORY TAGS from the vocal profile.
       - Use the instrumentation suggestions from the database.
       - Incorporate 2-3 sonic characteristics that fit the aesthetic archetypes.
       - If a fusion recipe is provided, incorporate its key elements.
       - Use technical audio engineering terms.
    
    2. LYRICS ({MAX_LYRIC_CHARS} chars max):
       - Structure: [Intro], [Verse 1], [Chorus], [Verse 2], [Bridge], [Outro].
       - Language: English.
       - MUST start with [START_ON: TRUE].
       - Content: Deep, metaphorical, avoiding clichés. Use "Show, Don't Tell" principle.
       - If scale/emotion mappings are provided, reflect that emotional tone in the lyrics.
       - If harmonic suggestions are provided, mention musical elements that align with them.

    3. TITLE:
       - Create a TITLE that is an IMPACTFUL SUMMARIZATION of what the song represents.
       - It should be catchy and resonant with the pop culture theme provided.

    OUTPUT FORMAT (JSON ONLY - NO MARKDOWN):
    {{
        "title": "Impactful Song Title",
        "style_prompt": "Technical style string with database elements",
        "lyrics": "Full lyrics with structure tags"
    }}
    """

# --- 5. FUNÇÃO DE GERAÇÃO (REQUEST HTTP) ---
def clean_json_response(text):
    """Limpa markdown que LLMs locais adoram colocar"""
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*$', '', text)
    return text.strip()

def gerar_lote_ollama(csv_path):
    print(f"\n🎹 MAESTRO AI (Enhanced): Initializing with model {MODEL_NAME}...")
    print("🖥️  GPU Optimization: Enabled for RTX 4070 Super")
    print("📚 Loading comprehensive music database...")
    
    # Inicializa o carregador de dados
    data_loader = MaestroDataLoader()
    print("✅ Database loaded successfully!\n")
    
    if not os.path.exists(csv_path):
        print(f"❌ Erro: Arquivo {csv_path} não encontrado.")
        return []

    # Lê o CSV
    df = pd.read_csv(csv_path)
    
    # Normalização de Dtypes
    if 'observacoes' in df.columns:
        df['observacoes'] = df['observacoes'].fillna('').astype(str)
    if 'status' in df.columns:
        df['status'] = df['status'].fillna('pending').astype(str)
    if 'titulo' in df.columns:
        df['titulo'] = df['titulo'].fillna('').astype(str)
    
    # Lógica de compatibilidade de colunas
    # V2 usa: album, titulo, tema, genero, mood, estetica, status, processada, observacoes
    # V1 usa: album, tema, estetica, processada, observacoes
    
    has_v2_cols = all(col in df.columns for col in ['genero', 'mood', 'titulo'])
    
    # Filtra apenas não processadas
    if 'processada' in df.columns:
        df_pendentes = df[df['processada'].str.lower() != 'sim'].copy()
    else:
        df_pendentes = df.copy() # Se não tem coluna, processa tudo
    
    if df_pendentes.empty:
        print("✅ Todas as músicas já foram processadas!")
        return []
    
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
            # Usa o título do CSV se disponível, caso contrário usa o tema
            display_title = row.get('titulo', row['tema']) if pd.notna(row.get('titulo')) else row['tema']
            print(f"   ➤ Compondo: [{row['album']}] - {display_title}...")
            
            # Carrega contexto inteligente de TODOS os arquivos JSON
            genre = str(row.get('genero', row.get('genre', 'Rock')))
            mood = str(row.get('mood', ''))
            gender = str(row.get('gender', 'male'))
            
            maestro_context = data_loader.build_context(
                row['tema'],
                row['estetica'],
                genre,
                gender,
                mood=mood
            )
            
            print(f"      📚 Context loaded: {len(maestro_context)} chars")
            
            # Adiciona contexto do álbum ao prompt
            # Passamos o título desejado para que o LLM possa refiná-lo ou usá-lo como base
            prompt = get_ollama_prompt(
                f"Album: {row['album']} | Title Intent: {display_title} | Inspiration: {row['tema']}", 
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
                    "num_ctx": 8192,        # Contexto massivo
                    "num_gpu": 99,          # Força GPU
                    "num_thread": 8         # Otimiza para CPU
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
                    "title": data.get('title', display_title),
                    "original_tema": row['tema'],
                    "genre": genre,
                    "mood": mood,
                    "style_prompt": final_style,
                    "lyrics": final_lyrics,
                    "status": "ready"
                }
                lote_pronto.append(track)
                
                # Marca como processada no DataFrame
                df.at[idx, 'processada'] = 'sim'
                df.at[idx, 'status'] = f"Success ({time.strftime('%Y-%m-%d %H:%M:%S')})"
                
                # Gera observações detalhadas para o CSV V2
                obs_list = [f"Genre: {genre}", f"Mood: {mood}"]
                # Tenta identificar o arquétipo usado para a observação
                archetype_context = data_loader.get_aesthetic_context(row['estetica'])
                if archetype_context:
                    arch_match = re.search(r'ARCHETYPE - (.*?)\]', archetype_context)
                    if arch_match:
                        obs_list.append(f"Aesthetic: {arch_match.group(1)}")
                
                df.at[idx, 'observacoes'] = " | ".join(obs_list)
                
                # Salva backup incremental do JSON V2
                with open('suno_batch_v2.json', 'w', encoding='utf-8') as f:
                    json.dump(lote_pronto, f, ensure_ascii=False, indent=2)
                
                # Atualiza o CSV após cada música processada
                df.to_csv(csv_path, index=False)
                
                duration = time.time() - start_time
                print(f"      ✅ Sucesso em {duration:.2f}s! Marcada como processada.")

            except requests.exceptions.Timeout:
                print(f"      ❌ Timeout: Modelo demorou mais de 180s")
                df.at[idx, 'status'] = "error: timeout"
                df.at[idx, 'observacoes'] = f"ERRO: Timeout em {time.strftime('%Y-%m-%d %H:%M:%S')}"
                df.to_csv(csv_path, index=False)
            except Exception as e:
                print(f"      ❌ Erro: {e}")
                df.at[idx, 'status'] = "error: crash"
                df.at[idx, 'observacoes'] = f"ERRO: {str(e)[:100]}"
                df.to_csv(csv_path, index=False)

    # Salva CSV final atualizado
    df.to_csv(csv_path, index=False)
    print(f"\n✅ Processamento concluído! {len(lote_pronto)} músicas geradas.")
    print(f"📁 Resultados salvos em: suno_batch_v2.json")
    print(f"📝 CSV atualizado: {csv_path}")
    print(f"\n✨ Execute 'maestro_brave_automator.py' para injetar no Suno.")
    
    return lote_pronto


# --- 7. EXPORTADOR DE LETRAS PARA MARKDOWN ---
def export_lyrics_to_markdown(json_path='suno_batch_v2.json', output_dir='lyrics'):
    """
    Exporta cada música do suno_batch_v2.json para arquivos markdown organizados.
    Estrutura: lyrics/{album}/{title}.md
    """
    import re
    
    if not os.path.exists(json_path):
        print(f"❌ Arquivo {json_path} não encontrado.")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        songs = json.load(f)
    
    if not songs:
        print("❌ Nenhuma música encontrada no batch.")
        return
    
    # Cria diretório base
    os.makedirs(output_dir, exist_ok=True)
    
    exported_count = 0
    
    for song in songs:
        try:
            album = song.get('album', 'Unknown Album')
            title = song.get('title', 'Untitled')
            genre = song.get('genre', 'Rock')
            mood = song.get('mood', 'N/A')
            style_prompt = song.get('style_prompt', '')
            lyrics = song.get('lyrics', '')
            
            # Sanitiza nome do arquivo (remove caracteres inválidos)
            safe_album = re.sub(r'[<>:"/\\|?*]', '', album)
            safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
            
            # Cria diretório do álbum
            album_dir = os.path.join(output_dir, safe_album)
            os.makedirs(album_dir, exist_ok=True)
            
            # Extrai BPM do style_prompt se disponível
            bpm_match = re.search(r'\[?(\d{2,3})\]?\s*BPM', style_prompt, re.IGNORECASE)
            bpm = bpm_match.group(1) if bpm_match else "120"
            
            # Extrai instrumentação do style_prompt
            instrumentation = "overdriven electric guitar, live acoustic drum kit, electric bass, dynamic vocals"
            instr_match = re.search(r'BPM[;\s]+([^;]+?)(?:;|\[|MANDATORY|$)', style_prompt)
            if instr_match:
                instrumentation = instr_match.group(1).strip()
            
            # Extrai tags vocais
            vocal_tags = "male vocals, aggressive, power belting, gritty distortion"
            vocal_match = re.search(r'(?:MANDATORY.*?TAGS?|Vocal Profile)[:\s]+([^\[\]]+?)(?:\[|$)', style_prompt, re.IGNORECASE)
            if vocal_match:
                vocal_tags = vocal_match.group(1).strip().rstrip(';,')
            
            # Constrói o markdown no formato do template
            md_content = f"""[Is_MAX_MODE: MAX](MAX)
[QUALITY: MAX](MAX)
[REALISM: MAX](MAX)
[REAL_INSTRUMENTS: MAX](MAX)
[GENRE]: {genre}
[MOOD]: {mood}
[BPM]: {bpm}
[INSTRUMENTATION]: {instrumentation}
[MANDATORY]: tight production, pristine clarity, professional mix
[SUNO_TAGS]: {vocal_tags}

[TITLE]: {title}
[Is_MAX_MODE: MAX](MAX)
[QUALITY: MAX](MAX)
[REALISM: MAX](MAX)
[REAL_INSTRUMENTS: MAX](MAX)
[START_ON: TRUE]

{lyrics}
"""
            
            # Salva o arquivo
            file_path = os.path.join(album_dir, f"{safe_title}.md")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            exported_count += 1
            
        except Exception as e:
            print(f"⚠️  Erro ao exportar '{title}': {e}")
    
    print(f"\n📝 Exportação concluída! {exported_count} arquivos criados em '{output_dir}/'")


if __name__ == "__main__":
    # Agora o padrão é o CSV V2 com novas colunas
    result = gerar_lote_ollama('fila_suno_v2.csv')
    
    # Exporta letras para markdown após geração
    if result:
        print("\n🎵 Exportando letras para arquivos Markdown...")
        export_lyrics_to_markdown()
    
    # Exporta letras para markdown após geração
    if result:
        print("\n🎵 Exportando letras para arquivos Markdown...")
        export_lyrics_to_markdown()
