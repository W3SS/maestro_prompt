import os
import time
import json
import pandas as pd
import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURAÇÃO ---
API_KEY = "AIzaSyB-diFX1yn0c6iH3v2TRM3x_QbquRVsswY"
genai.configure(api_key=API_KEY)

# --- CONFIGURAÇÕES DO SUNO (CONSTANTES) ---
MAX_LYRIC_CHARS = 4000  # Margem de segurança (Limite real 4000)
MAX_STYLE_CHARS = 900   # Limite rígido do Suno
MAX_MODE_HEADER = """[Is_MAX_MODE: MAX](MAX)
[QUALITY: MAX](MAX)
[REALISM: MAX](MAX)
[REAL_INSTRUMENTS: MAX](MAX)"""

# --- PERSONA MAESTRO & PROMPT ---
def get_maestro_prompt(tema, estetica_usuario, persona="MAESTRO AI"):
    return f"""
    IDENTIDADE: Você é o {persona} (Creative-Socratic).
    MISSÃO: Criar uma música para o Suno AI v5 com qualidade MAX MODE.
    
    ENTRADA DO USUÁRIO:
    - Tema: "{tema}"
    - Estética Desejada: "{estetica_usuario}"
    
    REGRAS RÍGIDAS (SUNO AI SPECS):
    1. STYLE PROMPT: Máximo {MAX_STYLE_CHARS} caracteres. Deve incluir tags técnicas de mixagem (ex: 'tape saturation', 'close mic'). NÃO use frases, use TAGS separadas por vírgula.
    2. LYRICS: Máximo {MAX_LYRIC_CHARS} caracteres. Estrutura obrigatória: [Intro], [Verse], [Chorus], etc.
    3. IDIOMA: Letras em INGLÊS (English).
    4. HEADER OBRIGATÓRIO: O campo de letras DEVE começar com a tag [START_ON: TRUE].
    
    ESTRATÉGIA DE REALISMO (MAX MODE):
    Use descritores como: "Room tone", "Natural dynamics", "Analog warmth", "Slight wow & flutter".
    
    SAÍDA ESPERADA (APENAS JSON):
    Retorne UM objeto JSON válido (sem markdown ```json) com as chaves:
    {{
        "title": "Título curto e impactante",
        "style_prompt": "String com tags técnicas e instrumentos (Inclua o BPM e Key no inicio)",
        "lyrics": "Letra completa formatada com quebras de linha \\n"
    }}
    """

# --- FUNÇÃO 1: GERADOR (GEMINI) ---
def gerar_lote_json(csv_path):
    print("--- 🎹 INICIANDO MAESTRO AI GENERATOR ---")
    df = pd.read_csv(csv_path)
    resultados = []
    
    model = genai.GenerativeModel('gemini-1.5-flash', 
                                  generation_config={"response_mime_type": "application/json"})

    for index, row in df.iterrows():
        print(f"Creatando track {index+1}/{len(df)}: {row['tema']}...")
        
        prompt = get_maestro_prompt(row['tema'], row['estetica'])
        
        try:
            response = model.generate_content(prompt)
            data = json.loads(response.text)
            
            # Pós-processamento para garantir limites e MAX MODE
            style_final = f"{MAX_MODE_HEADER}\n{data['style_prompt']}"
            if len(style_final) > MAX_STYLE_CHARS:
                style_final = style_final[:MAX_STYLE_CHARS]
            
            # Adicionar header de lyrics se não existir
            lyrics_final = data['lyrics']
            if "[Is_MAX_MODE: MAX]" not in lyrics_final:
                lyrics_final = f"{MAX_MODE_HEADER}\n\n[START_ON: TRUE]\n\n{lyrics_final}"

            track_data = {
                "id": index,
                "tema": row['tema'],
                "title": data['title'],
                "style_prompt": style_final,
                "lyrics": lyrics_final
            }
            resultados.append(track_data)
            time.sleep(4) # Rate limit safety
            
        except Exception as e:
            print(f"Erro no tema {row['tema']}: {e}")

    # Salva JSON intermediário
    with open('suno_batch.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Lote gerado! {len(resultados)} músicas salvas em suno_batch.json")
    return resultados

# --- FUNÇÃO 2: INJETOR (SELENIUM) ---
def injetar_no_suno(json_data):
    print("--- 🚀 INICIANDO INJEÇÃO AUTOMÁTICA NO SUNO ---")
    
    # Configura Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--user-data-dir=C:/Users/SEU_USUARIO/AppData/Local/Google/Chrome/User Data") # Opcional: Usar seu perfil real
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("[https://suno.com/create](https://suno.com/create)")
        
        print("\n⚠️  ATENÇÃO: Faça LOGIN manualmente no navegador aberto.")
        input("👉 Pressione ENTER aqui no terminal após logar e ver a tela 'Create'...")

        for track in json_data:
            print(f"Injetando: {track['title']}...")
            
            # 1. Ativar Custom Mode (se não estiver ativo)
            try:
                # Tenta encontrar o switch custom mode. Os seletores do Suno mudam, usar XPATH genérico é mais seguro
                # Procura por texto ou input checkbox
                custom_switch = driver.find_element(By.XPATH, "//input[@type='checkbox']") 
                if not custom_switch.is_selected():
                    custom_switch.click()
                    time.sleep(1)
            except:
                pass # Pode já estar aberto ou layout diferente

            # 2. Preencher Lyrics
            try:
                # Busca textarea de lyrics
                lyrics_box = driver.find_element(By.XPATH, "//textarea[contains(@placeholder, 'Enter your own lyrics')]")
                lyrics_box.clear()
                # Selenium send_keys pode ser lento com textos longos, usar JS é instantâneo
                driver.execute_script("arguments[0].value = arguments[1];", lyrics_box, track['lyrics'])
                lyrics_box.send_keys(" ") # Trigger de evento input
            except Exception as e:
                print(f"Erro ao preencher Lyrics: {e}")

            # 3. Preencher Style
            try:
                style_box = driver.find_element(By.XPATH, "//textarea[contains(@placeholder, 'Enter style of music')]")
                style_box.clear()
                # Limpa tags anteriores (MAX MODE ocupa espaço)
                driver.execute_script("arguments[0].value = arguments[1];", style_box, track['style_prompt'])
                style_box.send_keys(" ")
            except Exception as e:
                print(f"Erro ao preencher Style: {e}")

            # 4. Preencher Title
            try:
                title_box = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Enter a title')]")
                title_box.clear()
                title_box.send_keys(track['title'])
            except:
                pass

            # 5. Ação Final
            print(f"   -> {track['title']} preenchido. Revise e clique em Create.")
            input("👉 Pressione ENTER para injetar a próxima música (ou Ctrl+C para parar)...")
            
            # Opcional: Clicar no botão create automaticamente (Cuidado com gastos de crédito)
            # create_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Create')]")
            # create_btn.click()
            
            # Limpar campos para a próxima (recarregar página é mais seguro para limpar estados)
            driver.refresh()
            time.sleep(3)

    except Exception as e:
        print(f"Erro fatal no Selenium: {e}")
    finally:
        print("Finalizando automação...")
        driver.quit()

# --- EXECUÇÃO ---
if __name__ == "__main__":
    # 1. Cria CSV de exemplo se não existir
    if not os.path.exists('fila_suno.csv'):
        pd.DataFrame({
            'tema': ['Cyberpunk Redemption', 'Lovecraftian Void'],
            'estetica': ['Dark Synthwave, High BPM', 'Orchestral Doom Metal, Slow']
        }).to_csv('fila_suno.csv', index=False)
        print("Arquivo 'fila_suno.csv' criado. Edite-o e rode novamente.")
    else:
        # Modo Híbrido: Gera JSON e depois Injeta
        dados = gerar_lote_json('fila_suno.csv')
        injetar_no_suno(dados)