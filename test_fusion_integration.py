#!/usr/bin/env python3
"""Teste de integração do genre_fusion_matrix_enhanced.json"""

from maestro_ollama_enhanced import MaestroDataLoader

def test_enhanced_fusion_matrix():
    print("🧪 Testando integração do genre_fusion_matrix_enhanced.json\n")
    
    # Inicializa o loader
    print("1️⃣ Inicializando MaestroDataLoader...")
    loader = MaestroDataLoader()
    
    # Verifica se carregou as fusões
    fusion_recipes = loader.genre_fusion.get('genres', {}).get('fusion_recipes', [])
    total_fusions = len(fusion_recipes)
    
    print(f"✅ Fusões carregadas: {total_fusions}\n")
    
    # Testa novas fusões adicionadas
    print("2️⃣ Testando novas fusões adicionadas:")
    new_fusions = [
        "Progressive Deathcore",
        "Melodic Metalcore",
        "Bass House",
        "Melodic Dubstep",
        "Emo Rap",
        "Drill"
    ]
    
    for fusion_name in new_fusions:
        fusion = next((f for f in fusion_recipes if f['name'] == fusion_name), None)
        if fusion:
            print(f"   ✅ {fusion_name}")
            print(f"      Fórmula: {fusion.get('formula', 'N/A')}")
            if 'bpm_range' in fusion:
                print(f"      BPM: {fusion['bpm_range'][0]}-{fusion['bpm_range'][1]}")
            if 'artist_references' in fusion:
                artists = ', '.join(fusion['artist_references'][:2])
                print(f"      Artistas: {artists}")
            if 'difficulty' in fusion:
                print(f"      Dificuldade: {fusion['difficulty']}")
        else:
            print(f"   ❌ {fusion_name} - NÃO ENCONTRADO")
        print()
    
    # Testa fusões com metadados enhanced
    print("3️⃣ Testando fusões com metadados enhanced:")
    enhanced_fusions = ["Thall", "Trap Metal", "Djent"]
    
    for fusion_name in enhanced_fusions:
        fusion = next((f for f in fusion_recipes if f['name'] == fusion_name), None)
        if fusion:
            has_metadata = all(key in fusion for key in ['bpm_range', 'difficulty'])
            status = "✅" if has_metadata else "⚠️"
            print(f"   {status} {fusion_name}: Metadados {'completos' if has_metadata else 'parciais'}")
    
    print()
    
    # Testa método get_genre_fusion_recipe
    print("4️⃣ Testando get_genre_fusion_recipe:")
    recipe = loader.get_genre_fusion_recipe("Thall")
    if recipe:
        print(f"   ✅ Receita encontrada: {recipe.get('name')}")
        print(f"   Fórmula: {recipe.get('formula')}")
        print(f"   Elementos: {recipe.get('key_elements')}")
    else:
        print(f"   ❌ Receita não encontrada")
    
    print()
    
    # Estatísticas finais
    print("5️⃣ Estatísticas:")
    fusions_with_bpm = sum(1 for f in fusion_recipes if 'bpm_range' in f)
    fusions_with_artists = sum(1 for f in fusion_recipes if 'artist_references' in f)
    fusions_with_difficulty = sum(1 for f in fusion_recipes if 'difficulty' in f)
    
    print(f"   - Total de fusões: {total_fusions}")
    print(f"   - Com BPM range: {fusions_with_bpm}")
    print(f"   - Com artistas: {fusions_with_artists}")
    print(f"   - Com dificuldade: {fusions_with_difficulty}")
    
    print("\n✅ Teste concluído!")

if __name__ == "__main__":
    test_enhanced_fusion_matrix()
