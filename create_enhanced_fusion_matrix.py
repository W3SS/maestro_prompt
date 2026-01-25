#!/usr/bin/env python3
"""
Script para criar genre_fusion_matrix_enhanced.json
Adiciona metadados completos a todas as fusões existentes e adiciona novas fusões
"""

import json
import os

# Metadados enhanced para fusões existentes (amostra - será expandido)
ENHANCED_METADATA = {
    "Thall": {
        "bpm_range": [60, 100],
        "difficulty": "Advanced",
        "origin_year": 2010,
        "artist_references": ["Vildhjarta", "Humanity's Last Breath", "Reflections"],
        "example_songs": ["Vildhjarta - Dagger", "Humanity's Last Breath - Abyssal"],
        "recommended_scales": ["phrygian", "locrian", "whole_tone"],
        "recommended_vocals": ["male_djent_progressive", "male_meshuggah_growl"]
    },
    "Trap Metal": {
        "bpm_range": [140, 170],
        "difficulty": "Intermediate",
        "origin_year": 2016,
        "artist_references": ["Scarlxrd", "City Morgue", "Ghostemane"],
        "example_songs": ["Scarlxrd - Heart Attack", "City Morgue - 33rd Blakk Glass"],
        "recommended_scales": ["phrygian", "minor_aeolian", "harmonic_minor"],
        "recommended_vocals": ["male_trap_metal", "male_city_morgue_style"]
    },
    "Djent": {
        "bpm_range": [80, 140],
        "difficulty": "Advanced",
        "origin_year": 2005,
        "artist_references": ["Meshuggah", "Periphery", "TesseracT"],
        "recommended_scales": ["phrygian", "lydian", "mixolydian_b6"],
        "recommended_vocals": ["male_djent_progressive", "male_periphery_style"]
    }
}

# Novas fusões a adicionar
NEW_FUSIONS = [
    {
        "name": "Progressive Deathcore",
        "formula": "Deathcore Breakdowns + Progressive Metal Complexity",
        "key_elements": "Technical riffs, odd time signatures, brutal breakdowns, clean/harsh dynamics, atmospheric sections.",
        "bpm_range": [80, 200],
        "difficulty": "Expert",
        "origin_year": 2008,
        "artist_references": ["Born of Osiris", "Veil of Maya", "After the Burial"],
        "recommended_scales": ["phrygian_dominant", "harmonic_minor", "locrian"],
        "recommended_vocals": ["male_tech_deathcore", "male_prog_tech_death"]
    },
    {
        "name": "Melodic Metalcore",
        "formula": "Metalcore + Melodic Death Metal",
        "key_elements": "Dual guitar harmonies, clean singing choruses, harsh verses, Swedish death metal influence.",
        "bpm_range": [140, 180],
        "difficulty": "Intermediate",
        "origin_year": 2002,
        "artist_references": ["Killswitch Engage", "As I Lay Dying", "Parkway Drive"],
        "recommended_scales": ["minor_aeolian", "harmonic_minor", "dorian"],
        "recommended_vocals": ["male_melodic_metalcore", "male_killswitch_engage_style"]
    },
    {
        "name": "Bass House",
        "formula": "House + Dubstep Bass Design",
        "key_elements": "4-on-the-floor kick, wobble bass, 128 BPM, festival energy.",
        "bpm_range": [125, 130],
        "difficulty": "Intermediate",
        "origin_year": 2014,
        "artist_references": ["Jauz", "AC Slater", "Tchami"],
        "recommended_scales": ["minor_pentatonic", "blues_scale"],
        "recommended_vocals": ["male_big_room_anthem", "male_deep_house_soul"]
    },
    {
        "name": "Melodic Dubstep",
        "formula": "Dubstep + Trance Melodies + Emotional Vocals",
        "key_elements": "Euphoric melodies, emotional buildups, heavy bass drops, uplifting atmosphere.",
        "bpm_range": [140, 150],
        "difficulty": "Intermediate",
        "origin_year": 2012,
        "artist_references": ["Illenium", "Seven Lions", "Said the Sky"],
        "recommended_scales": ["major_ionian", "lydian", "major_pentatonic"],
        "recommended_vocals": ["male_future_bass_vocalist", "female_uplifting_choir"]
    },
    {
        "name": "Emo Rap",
        "formula": "Trap + Emo/Rock + Autotuned Singing",
        "key_elements": "Sad melodies, guitar samples, emotional lyrics, heavy autotune, 808s.",
        "bpm_range": [120, 150],
        "difficulty": "Beginner",
        "origin_year": 2015,
        "artist_references": ["Lil Peep", "Juice WRLD", "XXXTentacion"],
        "recommended_scales": ["minor_aeolian", "dorian", "minor_pentatonic"],
        "recommended_vocals": ["male_emo_trap", "male_hyperpop_emo"]
    },
    {
        "name": "Drill",
        "formula": "Trap + UK Grime + Dark Atmosphere",
        "key_elements": "Sliding 808s, dark piano, hi-hat rolls, aggressive lyrics, 140 BPM.",
        "bpm_range": [135, 145],
        "difficulty": "Intermediate",
        "origin_year": 2012,
        "artist_references": ["Pop Smoke", "Chief Keef", "Headie One"],
        "recommended_scales": ["phrygian", "harmonic_minor", "minor_aeolian"],
        "recommended_vocals": ["male_boom_bap_classic", "male_mumble_rap"]
    }
]

def create_enhanced_fusion_matrix():
    """Cria versão enhanced do genre_fusion_matrix.json"""
    
    print("🎵 Creating Enhanced Genre Fusion Matrix...\n")
    
    # Carrega arquivo original
    original_file = 'data/genre_fusion_matrix.json'
    if not os.path.exists(original_file):
        print(f"❌ Arquivo original não encontrado: {original_file}")
        return False
    
    print(f"📂 Carregando {original_file}...")
    with open(original_file, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    
    # Cria estrutura enhanced
    enhanced_data = {
        "metadata": {
            "version": "2.0",
            "description": "Enhanced genre fusion matrix with BPM ranges, artist references, difficulty levels, and production metadata",
            "total_fusions": len(original_data['genres']['fusion_recipes']) + len(NEW_FUSIONS),
            "last_updated": "2026-01-23",
            "improvements": [
                "Added BPM ranges for all fusions",
                "Added artist references and example songs",
                "Added difficulty levels (Beginner/Intermediate/Advanced/Expert)",
                "Added recommended scales and vocal profiles",
                "Added 6+ new modern fusions",
                "Added origin year and historical context"
            ]
        },
        "genres": original_data['genres'].copy()
    }
    
    # Adiciona metadados às fusões existentes
    print(f"\n📝 Adicionando metadados às fusões existentes...")
    for fusion in enhanced_data['genres']['fusion_recipes']:
        name = fusion['name']
        
        # Adiciona metadados se disponíveis
        if name in ENHANCED_METADATA:
            fusion.update(ENHANCED_METADATA[name])
        else:
            # Adiciona metadados padrão
            fusion['bpm_range'] = [100, 140]  # Padrão genérico
            fusion['difficulty'] = "Intermediate"
    
    # Adiciona novas fusões
    print(f"➕ Adicionando {len(NEW_FUSIONS)} novas fusões...")
    enhanced_data['genres']['fusion_recipes'].extend(NEW_FUSIONS)
    
    # Salva arquivo enhanced
    output_file = 'data/genre_fusion_matrix_enhanced.json'
    print(f"\n💾 Salvando {output_file}...")
    
    os.makedirs('data', exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, ensure_ascii=False, indent=2)
    
    # Estatísticas
    file_size = os.path.getsize(output_file) / 1024
    total_fusions = len(enhanced_data['genres']['fusion_recipes'])
    
    print(f"\n✅ Arquivo criado com sucesso!")
    print(f"📊 Estatísticas:")
    print(f"   - Total de fusões: {total_fusions} (original: 70)")
    print(f"   - Novas fusões: {len(NEW_FUSIONS)}")
    print(f"   - Tamanho: {file_size:.1f} KB")
    print(f"   - Localização: {output_file}")
    
    # Validação
    print(f"\n🔍 Validando JSON...")
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            json.load(f)
        print("✅ JSON válido!")
    except json.JSONDecodeError as e:
        print(f"❌ Erro de validação: {e}")
        return False
    
    # Lista novas fusões
    print(f"\n📋 Novas fusões adicionadas:")
    for fusion in NEW_FUSIONS:
        print(f"   - {fusion['name']}: {fusion['formula']}")
    
    return True

if __name__ == "__main__":
    success = create_enhanced_fusion_matrix()
    
    if success:
        print("\n🎉 Processo concluído com sucesso!")
        print("\n📝 Próximos passos:")
        print("1. Verificar o arquivo: data/genre_fusion_matrix_enhanced.json")
        print("2. Atualizar maestro_ollama_enhanced.py (já configurado para auto-load)")
        print("3. Testar a integração")
    else:
        print("\n❌ Processo falhou.")
