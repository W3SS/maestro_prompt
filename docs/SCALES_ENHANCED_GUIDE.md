# 🎼 Scales & Emotions Database - Enhanced Version

## 📊 O Que Foi Melhorado

### Versão Anterior (`scales_emotions.json`)

- ❌ Estrutura inconsistente (alguns usavam `emotions`, outros `psychoacoustics`)
- ❌ Sem referências de artistas
- ❌ Sem progressões de acordes
- ❌ Sem faixa de BPM
- ❌ Sem indicação de dificuldade
- ❌ Faltavam escalas importantes para metal moderno

### Versão Enhanced (`scales_emotions_enhanced.json`)

- ✅ **Estrutura 100% padronizada** para todas as escalas
- ✅ **Referências de artistas** (ex: "Metallica", "Meshuggah", "Opeth")
- ✅ **Progressões características** (ex: "i - bII - bVII - i")
- ✅ **Faixa de BPM sugerida** (ex: [140, 240])
- ✅ **Nível de dificuldade** (Beginner, Intermediate, Advanced, Expert)
- ✅ **Subgêneros de metal específicos** para cada escala
- ✅ **25 escalas** com dados completos
- ✅ **Novas escalas adicionadas**:
  - Mixolydian b6 (Aeolian Dominant) - Groove Metal
  - Phrygian Natural 3rd - Oriental Metal
  - Lydian Augmented - Progressive Metal
  - Dorian #4 (Ukrainian Dorian) - Folk Metal
  - Altered Dominant - Jazz Metal

## 📋 Estrutura de Cada Escala

```json
{
    "id": "phrygian_dominant",
    "name": "Phrygian Dominant",
    "intervals": [1, 3, 1, 2, 1, 2, 2],
    "psychoacoustics": {
        "primary_mood": "Epic/Exotic",
        "keywords": ["Middle-Eastern", "Intense", "Vampiric", "Dramatic", "Powerful"],
        "energy_level": "Very High"
    },
    "common_genres": ["Tech Death", "Symphonic Metal", "Psytrance", "Flamenco"],
    "lyrical_themes": ["Ancient Mythology", "Rituals", "Power", "Destruction"],
    "artist_references": ["Nile", "Behemoth", "Arch Enemy", "Yngwie Malmsteen"],
    "signature_chords": ["I - bII - I", "I - bII - bVII - I"],
    "bpm_range": [140, 260],
    "difficulty": "Advanced",
    "metal_subgenres": ["Technical Death Metal", "Symphonic Metal", "Neoclassical Metal"]
}
```

## 🎯 Como o Script Usa os Dados

### 1. Análise Inteligente de Tema

O script analisa palavras-chave no tema da música:

```python
# Exemplo: "Dark Magician"
emotion_keywords = {
    'dark': ['phrygian', 'locrian', 'harmonic_minor'],
    'evil': ['phrygian', 'phrygian_dominant'],
    'mysterious': ['whole_tone', 'lydian_dominant']
}
```

### 2. Mapeamento por Gênero

Escalas específicas para cada subgênero de metal:

```python
genre_scale_map = {
    'djent': ['phrygian', 'lydian', 'mixolydian_b6', 'octatonic_half_whole'],
    'death': ['phrygian', 'phrygian_dominant', 'harmonic_minor', 'locrian'],
    'doom': ['minor_aeolian', 'blues_scale', 'minor_pentatonic'],
    'thrash': ['phrygian', 'minor_aeolian', 'harmonic_minor']
}
```

### 3. Output Enriquecido

O contexto gerado agora inclui:

```
[SCALE/EMOTION MAPPING - Enhanced]
- **Phrygian** → Tension (Artists: Metallica, Slayer) | Chords: i - bII | Difficulty: Intermediate
- **Harmonic Minor** → Gothic Tension (Artists: Yngwie Malmsteen, Necrophagist) | Chords: i - V - i | Difficulty: Intermediate
- **Phrygian Dominant** → Epic/Exotic (Artists: Nile, Behemoth) | Chords: I - bII - I | BPM: 140-260 ✓ | Difficulty: Advanced
```

## 🎸 Escalas por Subgênero de Metal

### Djent

- **Phrygian** - Tensão agressiva
- **Lydian** - Seções atmosféricas
- **Mixolydian b6** - Grooves pesados
- **Octatonic** - Complexidade técnica

### Technical Death Metal

- **Phrygian Dominant** - Exotismo intenso
- **Harmonic Minor** - Tensão neoclássica
- **Super Locrian** - Dissonância extrema
- **Altered Dominant** - Complexidade jazzística

### Doom Metal

- **Minor Aeolian** - Melancolia pesada
- **Blues Scale** - Groove sludgy
- **Minor Pentatonic** - Simplicidade brutal
- **Phrygian** - Escuridão opressiva

### Progressive Metal

- **Lydian** - Atmosferas etéreas
- **Dorian** - Sofisticação groovy
- **Melodic Minor** - Mistério complexo
- **Lydian Dominant** - Tensão sonhadora

### Thrash Metal

- **Phrygian** - Agressão clássica
- **Minor Aeolian** - Melancolia rápida
- **Harmonic Minor** - Tensão neoclássica

## 📈 Benefícios para a Geração de Músicas

### Antes

```
[SCALE/EMOTION MAPPING]
- dark → Phrygian, Locrian, Harmonic Minor
```

### Depois

```
[SCALE/EMOTION MAPPING - Enhanced]
- **Phrygian** → Tension (Artists: Metallica, Slayer) | Chords: i - bII - bVII - i | Difficulty: Intermediate
- **Locrian** → Instability (Artists: Meshuggah, Gorguts) | Chords: i° - bII | Difficulty: Advanced
- **Harmonic Minor** → Gothic Tension (Artists: Yngwie Malmsteen, Necrophagist) | Chords: i - V - i | Difficulty: Intermediate
```

## 🔧 Integração no Maestro Enhanced

O método `get_scale_emotion_mapping()` agora:

1. ✅ Carrega automaticamente `scales_emotions_enhanced.json`
2. ✅ Analisa tema E gênero simultaneamente
3. ✅ Retorna até 3 escalas mais relevantes
4. ✅ Inclui artistas de referência
5. ✅ Mostra progressões de acordes
6. ✅ Indica BPM range (se disponível)
7. ✅ Mostra nível de dificuldade

## 💡 Exemplo de Uso

### Input CSV

```csv
album,tema,estetica,genre,gender
Cutthroat Tribe,Dark Magician,"Thrash/Djent fusion, occult",Djent,male
```

### Contexto Gerado

```
[VOCAL PROFILE - Spencer Sotelo (Periphery) style]
Description: Progressive metal with djent influence...
MANDATORY TAGS: male vocals, djent progressive, technical screams...

[GENRE FUSION RECIPE - Thall]
Formula: Djent + Ambience + Dissonance
Key Elements: Bending guitars, reverb washes, silence...

[INSTRUMENTATION]
low tuned 8-string guitar, noise gate, punchy mechanical drums...

[SONIC CHARACTERISTICS]
- brutal: Scooped mids, Gated drums, High-gain distortion...
- metallic: Comb filtering, Ring modulation, Cold high-mids...

[HARMONIC SUGGESTIONS]
- Minor key progressions, diminished chords, dark atmosphere

[SCALE/EMOTION MAPPING - Enhanced]
- **Phrygian** → Tension (Artists: Metallica, Slayer) | Chords: i - bII - bVII - i | Difficulty: Intermediate
- **Lydian** → Dreamy (Artists: Steve Vai, Dream Theater) | Chords: I - II - #IV | Difficulty: Intermediate
- **Mixolydian b6** → Dark Groove (Artists: Lamb of God, Gojira) | Chords: I - bVI - bVII | Difficulty: Intermediate
```

## 🎯 Próximas Melhorias Possíveis

1. **Adicionar mais escalas exóticas**:
   - Raga scales (Indian)
   - Maqam scales (Arabic)
   - Pentatonic variations

2. **Incluir exemplos de músicas**:
   - Nome da música + artista para cada escala

3. **Adicionar notação MIDI**:
   - Sequência de notas em MIDI numbers

4. **Progressões avançadas**:
   - Múltiplas progressões por escala
   - Variações modais

5. **Análise de tensão**:
   - Gráfico de tensão/resolução
   - Pontos de clímax harmônico

## 📚 Referências

- **Teoria Musical**: Escalas modais, harmonia funcional
- **Metal Moderno**: Djent, Technical Death, Progressive
- **Artistas**: Meshuggah, Gojira, Opeth, Nile, Behemoth, etc.
- **Produção**: BPM ranges típicos por subgênero

---

**Versão**: 2.0  
**Data**: 2026-01-23  
**Escalas Totais**: 25 (expandível)  
**Compatibilidade**: `maestro_ollama_enhanced.py`
