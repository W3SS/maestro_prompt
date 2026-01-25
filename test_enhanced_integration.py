#!/usr/bin/env python3
"""Teste de integração do vocal_profiles_enhanced.json"""

from maestro_ollama_enhanced import MaestroDataLoader

def test_enhanced_profiles():
    print("🧪 Testando integração do vocal_profiles_enhanced.json\n")
    
    # Inicializa o loader
    print("1️⃣ Inicializando MaestroDataLoader...")
    loader = MaestroDataLoader()
    
    # Verifica se carregou os perfis
    profiles = loader.vocal_profiles.get('vocal_characteristics_guide', {}).get('profiles', {})
    total_genres = len(profiles)
    
    print(f"✅ Perfis carregados: {total_genres} gêneros\n")
    
    # Testa gêneros novos que foram adicionados
    print("2️⃣ Testando novos gêneros adicionados:")
    new_genres = [
        ('Doom Metal', 'male'),
        ('Black Metal', 'male'),
        ('Grunge', 'male'),
        ('Punk', 'male'),
        ('Latin', 'male'),
        ('Country', 'male'),
        ('Djent', 'male'),
        ('Hyperpop', 'female')
    ]
    
    for genre, gender in new_genres:
        profile = loader.get_vocal_profile(genre, gender)
        if profile:
            desc = profile.get('description', 'N/A')
            tags = profile.get('suno_tags', 'N/A')
            print(f"   ✅ {genre} ({gender})")
            print(f"      Descrição: {desc[:80]}...")
            print(f"      Tags: {tags[:80]}...")
        else:
            print(f"   ❌ {genre} ({gender}) - NÃO ENCONTRADO")
        print()
    
    # Testa contexto completo
    print("3️⃣ Testando build_context completo:")
    context = loader.build_context(
        tema="Dark Ritual",
        estetica="Doom Metal, slow and heavy",
        genre="Doom Metal",
        gender="male"
    )
    
    print(f"   Tamanho do contexto: {len(context)} caracteres")
    print(f"   Preview:\n{context[:500]}...\n")
    
    # Estatísticas finais
    print("4️⃣ Estatísticas:")
    total_profiles = sum(len(variations) for variations in profiles.values())
    print(f"   - Total de gêneros: {total_genres}")
    print(f"   - Total de perfis: {total_profiles}")
    print(f"   - Média de variações por gênero: {total_profiles / total_genres:.1f}")
    
    # Lista alguns gêneros
    print(f"\n5️⃣ Exemplos de gêneros disponíveis:")
    for i, (genre, variations) in enumerate(list(profiles.items())[:15]):
        print(f"   {i+1}. {genre}: {len(variations)} variações")
    print(f"   ... e mais {total_genres - 15} gêneros")
    
    print("\n✅ Teste concluído com sucesso!")

if __name__ == "__main__":
    test_enhanced_profiles()
