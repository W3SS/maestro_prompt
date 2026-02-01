import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# --- CONFIGURAÇÃO DE AMBIENTE ---
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
GEMINI_URL = "https://gemini.google.com/app"

class GeminiAutomator:
    def __init__(self):
        options = Options()
        options.binary_location = BRAVE_PATH
        options.add_argument("--start-maximized")
        # Essencial para manter o login do Google AI Pro
        options.add_argument(f"--user-data-dir={os.path.join(os.getcwd(), 'gemini_profile')}") 
        
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def gerar_letra(self, prompt_final):
        self.driver.get(GEMINI_URL)
        time.sleep(3) # Aguarda carregamento inicial
        
        try:
            # Localiza a caixa de texto do Gemini (seletor de role textbox)
            input_box = self.driver.find_element(By.CSS_SELECTOR, "div[role='textbox']")
            input_box.clear()
            
            # Injeta o prompt estruturado
            self.driver.execute_script("arguments[0].innerText = arguments[1];", input_box, prompt_final)
            input_box.send_keys(Keys.SPACE) # Trigger para o botão de envio
            time.sleep(1)
            input_box.send_keys(Keys.ENTER)
            
            print("⏳ Gerando letra com Gemini Pro/Thinking...")
            # Aguarda o processamento (o botão de 'stop' sumir ou aparecer o botão de share)
            time.sleep(25) 
            
            # Captura a última resposta do modelo
            responses = self.driver.find_elements(By.CSS_SELECTOR, ".model-response-text")
            return responses[-1].text if responses else "Erro na captura."
            
        except Exception as e:
            return f"Erro na automação: {e}"

    def fechar(self):
        self.driver.quit()