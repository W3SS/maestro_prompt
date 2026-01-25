# 🎼 Maestro AI Ecosystem Guide

Este guia documenta o processo de desenvolvimento, configuração e resolução de problemas do ecossistema Maestro AI, otimizado para geração local via Ollama (Docker) e automação de injeção no Suno v5.

## 🛠️ Jornada de Desenvolvimento

O projeto evoluiu de um script simples baseado no Gemini para uma workstation neural híbrida local. Abaixo estão os marcos principais e as correções realizadas.

### 1. Desacoplamento de Componentes

Separamos o processo em dois estágios independentes:

- **Geração (Ollama)**: Focado em orquestrar dados musicais complexos e gerar estilos/letras via Mistral-Nemo.
- **Automação (Brave)**: Focado unicamente na injeção dos dados gerados na interface web do Suno.

### 2. Correções Técnicas Críticas

#### 🛑 Erros de Tipagem no Pandas

Identificamos um `TypeError` que ocorria quando o script tentava logar falhas (como timeouts do Ollama) na coluna `observacoes` do CSV.

- **Solução**: Forçamos a coluna `observacoes` a ser tratada como `string` (`astype(str)`) e preenchemos valores nulos com strings vazias, evitando que o Pandas inferisse tipos numéricos incorretos.

#### 🎼 Integridade do Banco de Dados Musical

O banco de dados de instrumentação (`instrument_specs.json`) possuía uma "trailing comma" (vírgula sobressalente) que impedia o carregamento do JSON.

- **Solução**: Realizamos a sanitização automatizada do arquivo, garantindo que o Maestro tenha acesso a todo o contexto de estilos (Djent, Shoegaze, Phonk, etc.).

#### 🐳 Suporte Híbrido ao Ollama (Nativo vs Docker)

Atualizamos o `start_maestro.bat` para detectar se o Ollama está rodando nativamente no Windows ou dentro de um container Docker.

- **Diferencial**: O script agora utiliza `docker exec` automaticamente se detectar o container `ollama` ativo, garantindo que o modelo `mistral-nemo:12b` esteja sempre disponível.

---

## 🚀 Como Executar o Ecossistema

### Pré-requisitos

- **Docker Desktop** rodando com suporte a WSL2.
- **Container Ollama** ativo (com nome `ollama`).
- **Python 3.8+**.

### Passo a Passo

1. **Inicie o Ambiente**: Execute `.\start_maestro.bat` no terminal.
2. **Configuração Automática**: O script cuidará do VENV, dependências e verificação do modelo.
3. **Geração**: O script `maestro_ollama_enhanced.py` processará a `fila_suno.csv`.
4. **Automação**: Ao final, escolha "S" quando perguntado se deseja rodar o automador do Brave para injetar as músicas no Suno.com.

---

## 📂 Estrutura de Arquivos (docs/)

- `DOCKER_WSL_SETUP.md`: Guia específico para configurar o container.
- `SCALES_ENHANCED_GUIDE.md`: Teoria musical aplicada ao Maestro.
- `VOCAL_PROFILES_ENHANCED_GUIDE.md`: Guia de personas vocais.
- `GENRE_FUSION_ANALYSIS.md`: Receitas de fusão de gêneros musicais.
- `INTEGRATION_GUIDE.md`: Detalhes sobre a ponte entre camadas.
