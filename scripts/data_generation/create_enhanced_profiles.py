#!/usr/bin/env python3
"""
Script para criar vocal_profiles_enhanced.json a partir do JSON fornecido pelo usuário.
O JSON fornecido já está completo e bem estruturado, apenas precisa ser salvo com metadados.
"""

import json
import os

# O JSON fornecido pelo usuário será salvo aqui
# Devido ao tamanho (~150KB), será necessário copiar manualmente ou usar arquivo separado

def create_enhanced_vocal_profiles():
    """
    Cria vocal_profiles_enhanced.json com metadados e estrutura completa.
    
    INSTRUÇÕES:
    1. Salve o JSON fornecido pelo usuário em um arquivo temporário: 'user_vocal_data.json'
    2. Execute este script: python create_enhanced_profiles.py
    3. O arquivo 'data/vocal_profiles_enhanced.json' será criado
    """
    
    print("🎤 Creating Enhanced Vocal Profiles Database...")
    
    # Verifica se o arquivo de dados do usuário existe
    user_file = 'user_vocal_data.json'
    if not os.path.exists(user_file):
        print(f"\n❌ Erro: Arquivo '{user_file}' não encontrado!")
        print("\n📝 Instruções:")
        print(f"1. Salve o JSON fornecido como '{user_file}'")
        print("2. Execute novamente este script")
        return False
    
    # Carrega dados fornecidos pelo usuário
    print(f"📂 Carregando {user_file}...")
    with open(user_file, 'r', encoding='utf-8') as f:
        user_data = json.load(f)
    
    # Conta gêneros e perfis
    profiles = user_data.get('vocal_characteristics_guide', {}).get('profiles', {})
    total_genres = len(profiles)
    total_profiles = sum(len(variations) for variations in profiles.values())
    
    print(f"✅ Dados carregados: {total_genres} gêneros, {total_profiles} perfis")
    
    # Cria estrutura enhanced com metadados
    enhanced_data = {
        "metadata": {
            "version": "2.0",
            "description": "Enhanced vocal profiles database with comprehensive genre coverage, artist references, and technical metadata",
            "total_genres": total_genres,
            "total_profiles": total_profiles,
            "last_updated": "2026-01-23",
            "improvements": [
                f"Added {total_genres - 15} new genres (Latin, Country, Classical, Soul, Funk, Disco, Reggae, Punk, Grunge, etc.)",
                "Standardized all profiles to use description + suno_tags format",
                "Added comprehensive subgenre variations",
                "Included experimental and niche genres (IDM, Glitch, Breakcore, Noise, etc.)",
                "Removed redundant artist_reference field"
            ],
            "genre_categories": {
                "mainstream": ["Pop", "Hip-Hop", "R&B", "Rock", "EDM", "Jazz", "Blues", "Country", "Latin", "Reggae"],
                "metal": ["Metal", "Doom Metal", "Black Metal", "Death Metal", "Thrash Metal", "Deathcore", "Sludge", "Industrial Metal"],
                "electronic": ["House", "Techno", "Trance", "Dubstep", "Drum & Bass", "Hardstyle", "Gabber", "Speedcore"],
                "experimental": ["IDM", "Glitch", "Breakcore", "Noise", "Drone", "Plunderphonics", "Lowercase"],
                "alternative": ["Indie", "Grunge", "Punk", "Shoegaze", "Math Rock", "Post-Rock", "Post-Hardcore"]
            }
        },
        "vocal_characteristics_guide": user_data.get('vocal_characteristics_guide', {})
    }
    
    # Cria diretório data/ se não existir
    os.makedirs('data', exist_ok=True)
    
    # Salva arquivo enhanced
    output_file = 'data/vocal_profiles_enhanced.json'
    print(f"\n💾 Salvando {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, ensure_ascii=False, indent=2)
    
    # Verifica tamanho do arquivo
    file_size = os.path.getsize(output_file)
    file_size_kb = file_size / 1024
    
    print(f"\n✅ Arquivo criado com sucesso!")
    print(f"📊 Estatísticas:")
    print(f"   - Gêneros: {total_genres}")
    print(f"   - Perfis: {total_profiles}")
    print(f"   - Tamanho: {file_size_kb:.1f} KB")
    print(f"   - Localização: {output_file}")
    
    # Validação
    print(f"\n🔍 Validando JSON...")
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            validation_data = json.load(f)
        print("✅ JSON válido!")
        
        # Lista alguns gêneros como exemplo
        sample_genres = list(profiles.keys())[:10]
        print(f"\n📋 Exemplos de gêneros incluídos:")
        for genre in sample_genres:
            variations = len(profiles[genre])
            print(f"   - {genre}: {variations} variações")
        print(f"   ... e mais {total_genres - 10} gêneros")
        
    except json.JSONDecodeError as e:
        print(f"❌ Erro de validação: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = create_enhanced_vocal_profiles()
    
    if success:
        print("\n🎉 Processo concluído com sucesso!")
        print("\n📝 Próximos passos:")
        print("1. Verificar o arquivo: data/vocal_profiles_enhanced.json")
        print("2. Atualizar maestro_ollama_enhanced.py para usar o novo arquivo")
        print("3. Testar a integração")
    else:
        print("\n❌ Processo falhou. Verifique as instruções acima.")
