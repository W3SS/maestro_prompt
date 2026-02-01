"""
MAESTRO BRAVE AUTOMATOR
-----------------------
Este script é responsável APENAS pela automação do browser (Brave/Chrome).
Ele lê o arquivo 'suno_batch.json' gerado pelo maestro_ollama_enhanced.py
e injeta os dados na interface web do Suno.

Dependências:
- selenium
- webdriver_manager
"""

import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# --- CONFIGURAÇÃO ---
# CAMINHO DO BRAVE (Ajuste conforme seu sistema operacional)
# Windows:
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
# Linux: "/usr/bin/brave-browser" 
# Mac: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

BATCH_FILE = 'suno_batch.json'

def carregar_lote():
    """Carrega o lote de músicas geradas."""
    if not os.path.exists(BATCH_FILE):
        print(f"❌ Arquivo {BATCH_FILE} não encontrado.")
        print("   Execute primeiro o 'maestro_ollama_enhanced.py' para gerar as músicas.")
        return []
    
    try:
        with open(BATCH_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"❌ Erro ao ler {BATCH_FILE}: {e}")
        return []

def abrir_brave_e_injetar(lote_dados):
    """Abre o Brave e injeta os dados do lote."""
    if not lote_dados:
        print("⚠️ Nenhum dado para injetar.")
        return

    print(f"\n🦁 INICIANDO AUTOMATOR ({len(lote_dados)} faixas)...")
    
    # Configuração Específica para Brave
    options = Options()
    options.binary_location = BRAVE_PATH 
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled") # Evita detecção básica
    
    # Inicializa Driver
    try:
        print("   Inicializando WebDriver...")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"❌ Erro ao abrir Brave. Verifique o caminho em BRAVE_PATH.")
        print(f"   Erro: {e}")
        return

    try:
        print("   Acessando Suno.com...")
        driver.get("https://suno.com/create")
        
        print("\n🛑 AÇÃO NECESSÁRIA: Faça LOGIN no Suno dentro do navegador aberto.")
        input("👉 Pressione ENTER aqui no terminal APÓS ver a tela de criação ('Create')...")

        for i, track in enumerate(lote_dados):
            print(f"\n💉 [{i+1}/{len(lote_dados)}] Injetando: {track.get('title', 'Untitled')}")
            
            # Validação básica
            if 'style_prompt' not in track or 'lyrics' not in track:
                print("   ⚠️ Faixa inválida (faltando style ou lyrics). Pulando...")
                continue

            # 1. Ativar Custom Mode
            try:
                # Procura switches (geralmente o Custom Mode é um toggle)
                switches = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
                custom_active = False
                
                # Tenta identificar se já está no modo custom (procurando campo de lyrics)
                try:
                    driver.find_element(By.XPATH, "//textarea[contains(@placeholder, 'Enter your own lyrics')]")
                    custom_active = True
                except:
                    pass
                
                if not custom_active:
                    for sw in switches:
                        # Tenta clicar no primeiro switch não marcado
                        if not sw.is_selected():
                            sw.click()
                            time.sleep(0.5)
                            break 
            except Exception as e: 
                print(f"   ⚠️ Aviso no Custom Mode: {e}")

            # 2. Injetar Letra
            try:
                lyrics_box = driver.find_element(By.XPATH, "//textarea[contains(@placeholder, 'Enter your own lyrics')]")
                # Limpa e injeta
                lyrics_box.clear()
                driver.execute_script("arguments[0].value = arguments[1];", lyrics_box, track['lyrics'])
                lyrics_box.send_keys(" ") # Trigger event
            except: 
                print("   ❌ ERRO: Campo de Lyrics não encontrado.")

            # 3. Injetar Estilo
            try:
                style_box = driver.find_element(By.XPATH, "//textarea[contains(@placeholder, 'Enter style of music')]")
                style_box.clear() 
                driver.execute_script("arguments[0].value = arguments[1];", style_box, track['style_prompt'])
                style_box.send_keys(" ")
            except:
                print("   ❌ ERRO: Campo de Estilo não encontrado.")

            # 4. Injetar Título
            try:
                title_box = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Enter a title')]")
                title_box.clear()
                driver.execute_script("arguments[0].value = arguments[1];", title_box, track.get('title', ''))
                title_box.send_keys(" ")
            except: 
                pass

            print(f"   ✅ Injeção concluída!")
            
            if i < len(lote_dados) - 1:
                input("👉 Pressione ENTER para a próxima música (ou Ctrl+C para encerrar)...")
                driver.refresh()
                time.sleep(2)
            else:
                print("\n🏁 Lote finalizado!")
                input("👉 Pressione ENTER para fechar o navegador...")

    except Exception as e:
        print(f"\n❌ Erro durante automação: {e}")
    finally:
        print("Encerrando driver...")
        driver.quit()

if __name__ == "__main__":
    dados = carregar_lote()
    if dados:
        abrir_brave_e_injetar(dados)