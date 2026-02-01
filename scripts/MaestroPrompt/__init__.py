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

# --- CONFIGURATION ---
API_KEY = "[ENCRYPTION_KEY]"
genai.configure(api_key=API_KEY)

# --- SUNO CONFIGURATIONS (CONSTANTS) ---
MAX_LYRIC_CHARS = 4000 # Safety margin (Actual limit 4000)
MAX_STYLE_CHARS = 900 # Suno hard limit
MAX_MODE_HEADER = """[Is_MAX_MODE: MAX](MAX)
[QUALITY: MAX](MAX)
[REALISM: MAX](MAX)
[REAL_INSTRUMENTS: MAX](MAX)"""

# --- MAESTRO PERSONA & PROMPT ---
def get_maestro_prompt(theme, user_aesthetics, persona="MAESTRO AI"):

    return f"""

      IDENTITY: You are the {persona} (Creative-Socratic).

      MISSION: Create a song for Suno AI v5 with MAX MODE quality.

      USER INPUT:

      - Theme: "{theme}"
      - Desired Aesthetics: "{user_aesthetics}"

      STRICT RULES (SUNO AI SPECS):

      1. STYLE PROMPT: Maximum {MAX_STYLE_CHARS} characters. Must include technical mixing tags (e.g., 'tape saturation', 'close mic'). DO NOT use phrases, use TAGS separated by commas.
      2. LYRICS: Maximum {MAX_LYRIC_CHARS} characters. Mandatory structure: [Intro], [Verse], [Chorus], etc.
      3. LANGUAGE: Lyrics in ENGLISH.
      4. MANDATORY HEADER: The lyrics field MUST start with the tag [START_ON: TRUE].

      REALISM STRATEGY (MAX MODE):
      Use descriptors such as: "Room tone", "Natural dynamics", "Analog warmth", "Slight wow & flutter".

      EXPECTED OUTPUT (JSON ONLY):
      Return ONE valid JSON object (without markdown ```json) with the following keys:

      {{
        "title": "Short and impactful title",
        "style_prompt": "String with technical tags and instruments (Include BPM and Key at the beginning)",
        "lyrics": "Full lyrics formatted with line breaks \\n"
      }}

    """

# --- FUNCTION 1: GENERATOR (GEMINI) ---
def generate_batch_json(csv_path): 
  print("--- 🎹 STARTING MAESTRO AI GENERATOR ---") 
  df = pd.read_csv(csv_path) 
  results = [] 

  model = genai.GenerativeModel('gemini-1.5-flash', 
  generation_config={"response_mime_type": "application/json"}) 

  for index, row in df.iterrows(): 
    print(f"Creating track {index+1}/{len(df)}: {row['tema']}...") 

    prompt = get_maestro_prompt(row['tema'], row['estetica']) 

    try: 
      response = model.generate_content(prompt) 
      date = json.loads(response.text) 

      # Post-processing to ensure limits and MAX MODE 
      style_final = f"{MAX_MODE_HEADER}\n{data['style_prompt']}" 
      if len(style_final) > MAX_STYLE_CHARS: 
        style_final = style_final[:MAX_STYLE_CHARS] 

      # Add lyrics header if it doesn't exist 
      lyrics_final = data['lyrics'] 
      if "[Is_MAX_MODE: MAX]" not in lyrics_final: 
        lyrics_final = f"{MAX_MODE_HEADER}\n\n[START_ON: TRUE]\n\n{lyrics_final}" 

      track_data = { 
        "id": index, 
        "theme": row['theme'], 
        "title": data['title'], 
        "style_prompt": style_final, 
        "lyrics": lyrics_final
      }
      results.append(track_data)

      time.sleep(4) # Rate limit safety

    except Exception as e:

      print(f"Error in theme {row['theme']}: {e}")

      # Saves intermediate JSON

      with open('suno_batch.json', 'w', encoding='utf-8') as f:

        json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"✅ Batch generated! {len(results)} songs saved in suno_batch.json")

        return results

# --- FUNCTION 2: INJECTOR (SELENIUM) ---
def inject_into_suno(json_data):

  print("--- 🚀 STARTING AUTOMATIC INJECTION IN SUNO ---")

  # Configure Chrome
  options = webdriver.ChromeOptions()

  options.add_argument("--start-maximized")
  # options.add_argument("--user-data-dir=C:/Users/YOUR_USERNAME/AppData/Local/Google/Chrome/User Data") # Optional: Use your real profile
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

  try:

    driver.get("[https://suno.com/create](https://suno.com/create)")
    print("\n⚠️ WARNING: Do LOG IN manually in the open browser.")
    input("👉 Press ENTER here in the terminal after logging in and seeing the 'Create' screen...")

    for track in json_data:

      print(f"Injecting: {track['title']}...")

      # 1. Enable Custom Mode (if not already enabled)

      try:

        # Attempts to find the custom mode switch. Suno selectors change, using generic XPath is safer
        # Search for text or checkbox input

        custom_switch = driver.find_element(By.XPATH, "//input[@type='checkbox']")
        if not custom_switch.is_selected():

          custom_switch.click()
          time.sleep(1)

      except:
        pass # May already be open or have a different layout

      # 2. Fill Lyrics
      try:

        # Search for lyrics textarea
        lyrics_box = driver.find_element(By.XPATH, "//textarea[contains(@placeholder, 'Enter your own lyrics')]")
        lyrics_box.clear()

        # Selenium send_keys can be slow with long texts, using JS is instantaneous
        driver.execute_script("arguments[0].value = arguments[1];", lyrics_box, track['lyrics']) 
        lyrics_box.send_keys(" ") # Input event trigger 
      except Exception as e: 
        print(f"Error filling Lyrics: {e}") 

      # 3. Fill Style 
      try: 
        style_box = driver.find_element(By.XPATH, "//textarea[contains(@placeholder, 'Enter style of music')]") 
        style_box.clear() 
        # Clear previous tags (MAX MODE takes up space) 
        driver.execute_script("arguments[0].value = arguments[1];", style_box, track['style_prompt']) 
        style_box.send_keys(" ") 
      except Exception as e: 
        print(f"Error filling Style: {e}") 

      # 4. Fill Title 
      try: 
        title_box = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Enter a title')]")
        title_box.clear()
        title_box.send_keys(track['title'])
      except:
        pass

      # 5. Final Action

      print(f" -> {track['title']} filled. Review and click Create.")
      input("👉 Press ENTER to inject the next song (or Ctrl+C to stop)...")

      # Optional: Click the create button automatically (Beware of credit usage)
      # create_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Create')]")
      # create_btn.click()
      # Clear fields for the next one (reloading the page is safer for clearing states)
      driver.refresh()

      time.sleep(3)

    except Exception as e:

      print(f"Fatal error in Selenium: {e}")
    finally:

      print("Finishing automation...")

      driver.quit()

  # --- EXECUTION ---
  if __name__ == "__main__":

  # 1. Creates example CSV if it doesn't exist

    if not os.path.exists('fila_suno.csv'):
      pd.DataFrame({
      'theme': ['Cyberpunk Redemption', 'Lovecraftian Void'],
      'aesthetics': ['Dark Synthwave, High BPM', 'Orchestral Doom Metal, Slow']
      }).to_csv('fila_suno.csv', index=False)
      print("File 'fila_suno.csv' created. Edit it and run again.")

    else:

      # Hybrid Mode: Generates JSON and then injects
      data = generate_batch_json('fila_suno.csv')
      inject_into_suno(data)