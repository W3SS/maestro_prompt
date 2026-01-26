# Insights: Maestro AI Development & Improvements

Durante a validação do pipeline de geração de álbuns multi-gênero (Grunge, Black Metal, Pop), vários insights técnicos e arquiteturais foram identificados.

## Análise de Performance Técnica

### 1. Latência de Modelos Grandes (Mistral-Nemo 12B)

- **Observação**: O design de um álbum de 8 faixas ou a geração de um único prompt complexo excedeu frequentemente os timeouts padrão de 60s e até 180s.
- **Causa Raiz**: O ambiente de CPU de 4 núcleos, combinado com alto contexto (8k) e um modelo de 12b, resulta em uma inferência lenta.
- **Melhoria**:
  - Implementar um **timeout base de 1300s** para todas as chamadas de LLM.
  - Considerar o uso de **Streaming Responses** para dar feedback em tempo real e evitar timeouts silenciosos.

### 2. Gestão de Contexto

- **Observação**: Carregar toda a base de semiótica, escalas e instrumentos para cada geração de faixa é redundante e aumenta o peso do payload.
- **Melhoria**:
  - Implementar um **Context Cache** ou uma lógica de **Smart Pruning** que injete apenas os segmentos JSON relevantes ao arquétipo/gênero específico da faixa.

### 3. Recuperação de Erros

- **Observação**: Flutuações de rede ou estados de ocupação do Ollama levam a falhas/retentativas manuais.
- **Melhoria**:
  - Implementar **Exponential Backoff** para requisições HTTP.
  - Salvar um **Mapa de Estado (Checkpoints)** para que o script possa retomar exatamente de onde parou.

## Recomendações Arquiteturais

- [ ] **Estratégia de Dois Modelos**: Usar um modelo mais rápido (ex: Llama-3 8b) para o design da estrutura do álbum e um mais criativo (12b+) para letras e prompts complexos.
- [ ] **I/O Assíncrono**: Refatorar o loop principal para usar `asyncio` e lidar melhor com a fila de geração.
- [ ] **Camada de Validação**: Implementar validação baseada em Pydantic antes de salvar no `suno_batch_v2.json` para garantir erro-zero na injeção final.

---
*Gerado por Antigravity durante a fase de validação do Maestro.*
