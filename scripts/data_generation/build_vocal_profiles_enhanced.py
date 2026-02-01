import json
import os

# Script para criar vocal_profiles_enhanced.json com todos os dados fornecidos pelo usuário
# mais as melhorias sugeridas na análise

def create_enhanced_vocal_profiles():
    """Cria versão enhanced do vocal_profiles.json"""
    
    # Carrega o JSON fornecido pelo usuário (será criado manualmente devido ao tamanho)
    # Este script serve como template para a estrutura enhanced
    
    enhanced_structure = {
        "metadata": {
            "version": "2.0",
            "description": "Enhanced vocal profiles database with comprehensive genre coverage, artist references, and technical metadata",
            "total_genres": 60,
            "total_profiles": "200+",
            "last_updated": "2026-01-23",
            "improvements": [
                "Added 40+ new genres (Latin, Country, Classical, Soul, Funk, Disco, Reggae, Punk, Grunge, etc.)",
                "Removed artist_reference field (redundant with description)",
                "Standardized all profiles to use description + suno_tags format",
                "Added comprehensive subgenre variations",
                "Included experimental and niche genres"
            ]
        },
        "vocal_characteristics_guide": {
            "description": "Comprehensive guide of vocal profiles for Suno AI generation, separated by genre and gender, focusing on technical characteristics and timbres. Includes multiple variations with distinctive characteristics.",
            "usage_guide": {
                "how_to_select": "Match genre + gender + specific style variation based on song requirements",
                "format": "Each profile contains 'description' (technical details) and 'suno_tags' (AI generation tags)",
                "note": "Profiles without artist_reference field are intentional - descriptions are self-contained"
            },
            "profiles": {
                # O conteúdo completo fornecido pelo usuário será inserido aqui
                # Devido ao tamanho, será feito em etapas
            }
        }
    }
    
    print("Enhanced vocal profiles structure created")
    print(f"Total expected genres: {enhanced_structure['metadata']['total_genres']}")
    print(f"Total expected profiles: {enhanced_structure['metadata']['total_profiles']}")
    
    return enhanced_structure

if __name__ == "__main__":
    structure = create_enhanced_vocal_profiles()
    print("\n✅ Template created successfully")
    print("\n📝 Next step: Merge user-provided JSON content into profiles section")

