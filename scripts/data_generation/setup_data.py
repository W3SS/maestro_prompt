import os
import json
import pandas as pd

# --- DADOS CONSOLIDADOS (Baseado nos seus Uploads) ---
VOCAL_DATA = ''

KNOWLEDGE_DATA = {
  "sonic_characteristics": {
    "clean": "Audiophile reference quality, Transparent and uncolored, Full dynamic range.",
    "glossy": "Hyper-compressed, Autotune polish, Bright high-end, Digital precision.",
    "gritty": "Tube saturation, Vinyl crackle, Room bleed, Tape hiss, Mid-range focus.",
    "brutal": "Scooped mids, Gated drums, High-gain distortion, Aggressive transient shaping.",
    "ethereal": "Massive hall reverb, Shimmer delay, Washed-out transients, Floating atmosphere.",
    "cyber": "Bitcrushed textures, Glitch artifacts, Granular synthesis, Robotic vocal chains.",
    "warm": "Analog warmth, Round bass, Smooth treble roll-off, Ribbon microphone character.",
    "kinetic": "Transient heavy, Sidechain pumping, Dry percussion, Tight rhythmic pocket.",
    "abyssal": "Sub-bass pressure, cavernous reverb, Low-pass filtering, Slow movement."
  },
  "genre_fusion_recipes": {
    "Thall": "Djent + Ambience + Dissonance: Pitch-shifted delays, bending guitars.",
    "Trap Metal": "Trap 808s + Screaming Vocals: Distortion, simple flow, clipped bass.",
    "Glitchcore": "Pop Melodies + IDM Glitches: Sped up vocals, bitcrushing, bubblegum synths.",
    "Dungeon Synth": "Black Metal Atmosphere + Lo-Fi Synths: Medieval scales, low fidelity.",
    "Blackgaze": "Black Metal Blast Beats + Shoegaze Wall of Sound: Tremolo picking, major key melodies.",
    "Phonk": "Memphis Rap Vocals + Cowbells + Trap Beats: Sidechain compression, lo-fi grit.",
    "Hyperpop": "Pop Melodies + Industrial Noise: Extreme autotune, pitched vocals, chaotic structure.",
    "Djent/Metalcore": "Technical precision + Emotional dynamics: Polyrhythms, breakdowns, clean/scream contrast.",
    "Industrial Metal": "Mechanical rhythms + Heavy guitars: Synth layers, distorted vocals, dystopian atmosphere.",
    "Deathcore": "Death Metal brutality + Hardcore breakdowns: Guttural vocals, blast beats, crushing heaviness."
  }
}

def setup():
    print("\n🎵 MAESTRO SUNO SETUP - Criando estrutura de dados...\n")
    
    # 1. Criar Pastas
    os.makedirs("data", exist_ok=True)
    print("✅ Pasta 'data/' criada.")

    # 2. Gerar JSONs
    with open("data/vocal_profiles.json", "w", encoding="utf-8") as f:
        json.dump(VOCAL_DATA, f, indent=2, ensure_ascii=False)
    print("✅ data/vocal_profiles.json gerado.")

    with open("data/maestro_knowledge.json", "w", encoding="utf-8") as f:
        json.dump(KNOWLEDGE_DATA, f, indent=2, ensure_ascii=False)
    print("✅ data/maestro_knowledge.json gerado.")
    
    # Também cria na raiz para compatibilidade
    with open("vocal_profiles.json", "w", encoding="utf-8") as f:
        json.dump(VOCAL_DATA, f, indent=2, ensure_ascii=False)
    print("✅ vocal_profiles.json (raiz) gerado.")

    with open("maestro_knowledge.json", "w", encoding="utf-8") as f:
        json.dump(KNOWLEDGE_DATA, f, indent=2, ensure_ascii=False)
    print("✅ maestro_knowledge.json (raiz) gerado.")

    print("\n🚀 Setup concluído! Arquivos JSON criados com sucesso.")
    print("📝 Agora você pode executar 'maestro_ollama.py' ou 'maestro_brave_automator.py'")

if __name__ == "__main__":
    setup()
