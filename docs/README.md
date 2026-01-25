# 🎵 Maestro Suno Automation Suite

Sistema completo para geração automatizada de músicas usando IA (Gemini/Ollama) e injeção automática no Suno.com.

## 📁 Arquivos do Sistema

| Arquivo | Descrição |
|---------|-----------|
| `maestro_brave_automator.py` | Script principal com Gemini AI + Selenium/Brave |
| `maestro_ollama.py` | Versão local usando Ollama (sem API externa) com carregamento inteligente de dados |
| `setup_data.py` | Script de setup para criar arquivos JSON de dados |
| `fila_suno.csv` | Fila de músicas com 37 tracks em 4 álbuns |
| `suno_batch.json` | Output JSON com músicas processadas |
| `data/vocal_profiles.json` | Perfis vocais por gênero e gênero |
| `data/maestro_knowledge.json` | Características sônicas e receitas de fusão |

## 🎸 Álbuns Disponíveis

### Human Being (Djent/Metalcore) - 10 tracks

Temas existenciais, progressivo, dinâmicas clean/scream

### Orichalcum (Deathcore) - 8 tracks

Apocalipse, horror, breakdowns brutais

### Dark Core (Industrial Metal) - 9 tracks

Distopia tecnológica, mecânico, sintetizadores

### Cutthroat Tribe (Thrash/Djent Fusion) - 8 tracks

Crítica social, energia thrash 80s/90s com precisão djent

## 🚀 Como Usar

### Opção 1: Gemini API (Cloud)

```bash
python maestro_brave_automator.py
```

**Requisitos:**

- API Key do Gemini configurada
- Conexão com internet
- Brave Browser instalado

### Opção 2: Ollama (Local)

```bash
python maestro_ollama.py
```

**Requisitos:**

- Ollama rodando localmente (`ollama serve`)
- Modelo baixado (`ollama pull mistral-nemo:12b`)
- Sem necessidade de API externa

## ✨ Recursos Implementados

### ✅ Validação de Colunas

- Verifica colunas obrigatórias: `album`, `tema`, `estetica`, `processada`
- Retorna erro descritivo se faltar alguma

### ✅ Filtro de Processadas

- Ignora automaticamente tracks com `processada = 'sim'`
- Mostra contador de pendentes vs. totais

### ✅ Agrupamento por Álbum

- Processa músicas agrupadas por álbum
- Mantém consistência temática
- Adiciona contexto do álbum ao prompt

### ✅ Atualização Automática

- Marca músicas como processadas após sucesso
- Adiciona timestamp nas observações
- Registra erros se houver falha
- Salva após cada música (segurança)

## 📊 Estrutura do CSV

```csv
album,tema,estetica,processada,observacoes
Human Being,Imitation of Life,"Persona: AUREN VALENTINE (Djent/Metalcore), 140 BPM...",nao,
```

**Colunas:**

- `album`: Nome do álbum
- `tema`: Título/tema da música
- `estetica`: Descrição detalhada do estilo (persona, BPM, instrumentação)
- `processada`: Status (`nao` ou `sim`)
- `observacoes`: Timestamp ou mensagens de erro

## 🔧 Configuração

### Gemini API Key

Edite `maestro_brave_automator.py` linha 13:

```python
API_KEY = "SUA_API_KEY_AQUI"
```

### Ollama Model

Edite `maestro_ollama.py` linha 16:

```python
MODEL_NAME = "mistral-nemo:12b"  # ou phi3.5, qwen2.5:7b
```

### Brave Browser Path

Edite `maestro_brave_automator.py` linha 18:

```python
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
```

## 📝 Workflow Completo

1. **Editar CSV**: Adicione/edite músicas em `fila_suno.csv`
2. **Gerar Conteúdo**: Execute `maestro_ollama.py` ou `maestro_brave_automator.py`
3. **Verificar JSON**: Revise `suno_batch.json` gerado
4. **Injetar no Suno**: O script abre Brave e injeta automaticamente
5. **Login Manual**: Faça login no Suno quando solicitado
6. **Revisar e Criar**: Revise cada música e clique em "Create"

## ⚠️ Troubleshooting

### Erro: "429 You exceeded your current quota"

- **Solução**: Aguarde reset diário ou crie nova API key em [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Alternativa**: Use `maestro_ollama.py` (100% local)

### Erro: "Connection refused" (Ollama)

```bash
# Inicie o Ollama primeiro
ollama serve

# Em outro terminal, baixe o modelo
ollama pull mistral-nemo:12b
```

### Erro: "Brave not found"

- Verifique o caminho do Brave em `BRAVE_PATH`
- Windows: Geralmente em `C:\Program Files\BraveSoftware\...`

## 🎯 Próximas Melhorias

- [ ] Mover API key para variável de ambiente
- [ ] Adicionar argumento CLI para processar álbum específico
- [ ] Implementar retry automático em caso de erro
- [ ] Preview das músicas antes de injetar
- [ ] Relatório HTML com estatísticas

## 📄 Licença

Projeto pessoal - Use livremente
