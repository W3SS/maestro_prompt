# 🐳 Setup do Ollama com Docker e WSL (Opcional)

Este guia explica como configurar o Ollama rodando dentro de um container Docker no WSL2, que é a configuração recomendada para máxima performance e isolamento no Windows.

## 📋 Pré-requisitos

1. **WSL2 Instalado**:
    * Abra o PowerShell como Admin e execute: `wsl --install`
    * Reinicie o computador.

2. **Docker Desktop Instalado**:
    * Baixe e instale o [Docker Desktop para Windows](https://www.docker.com/products/docker-desktop/).
    * Nas configurações do Docker (General), marque a opção "Use the WSL 2 based engine".
    * Em "Resources > WSL Integration", ative a integração com sua distro principal (ex: Ubuntu).

## 🚀 Instalação Manual via CLI

O script `start_maestro.sh` tenta fazer isso automaticamente, mas aqui está o processo manual:

### 1. Verificar se o Docker está rodando no WSL

Abra seu terminal WSL (Ubuntu) e execute:

```bash
docker --version
```

### 2. Rodar o container Ollama (Versão CPU/GPU)

Para criar o container persistente:

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### 3. Baixar o Modelo

Com o container rodando:

```bash
docker exec -it ollama ollama pull mistral-nemo:12b
```

## 🛠️ Resolução de Problemas

* **Erro "H:\Meu Drive"**: No WSL, o drive `H:` é montado em `/mnt/h`. Se estiver rodando scripts Python dentro do WSL, use o caminho Linux.
* **Porta em Uso**: Se o Ollama nativo do Windows estiver rodando, ele pode conflitar na porta 11434. Feche o app Windows antes de rodar o container.
