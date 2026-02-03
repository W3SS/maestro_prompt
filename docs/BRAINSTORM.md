# 🧠 BRAINSTORM: Song Reverse Engineering Feature

> **Date:** 2026-02-02
> **Participants:** Project Owner (PO), Backend Specialist (BE), UI/UX Designer (UX)
> **Goal:** Definir a feature de "Engenharia Reversa Musical" (DNA Extraction) e integrá-la ao ecossistema Maestro AI.

---

## 1. 💡 The Concept (Vision)

**PO:** "Eu quero que o usuário digite 'Bohemian Rhapsody' e o sistema entenda *profundamente* o que faz essa música funcionar (ópera + rock, estrutura complexa, harmonias vocais) e use isso para criar algo novo, mas com essa mesma 'alma'."

**UX:** "Para o usuário, deve ser mágico. Um input simples de busca, seguido de uma visualização incrível do 'DNA' da música sendo decodificado, e um botão: 'Gerar Variações'."

**BE:** "Tecnicamente, podemos usar o LLM (que já temos integrado) como motor de inferência. Ele conhece a teoria musical de músicas famosas. O desafio é mapear esse conhecimento não-estruturado para nossos JSONs estruturados em `data/`."

### Value Proposition & Monetization 💰

* **Free Tier:** Análise básica (Gênero + Mood). Geração simples.
* **Pro Tier ($):** "Deep DNA" (Extração de Instrumentação específica, Progressão Harmônica exata, Técnicas de Produção de `audio_specs.json`).
* **Enterprise ($$$):** "Style Cloning" para bibliotecas de produção em massa.

---

## 2. 🏗️ Architecture & Implementation

### Data Flow

1. **Input:** `query="Song Name - Artist"`
2. **Analysis Agent (Backend):**
    * Consulta LLM (Gemini/Ollama) pedindo análise estruturada.
    * Prompt System: "Analise a música X. Mapeie para os parâmetros: sonic_characteristics (de `audio_specs.json`), genre_fusion (de `genre_fusion_matrix.json`), mood."
3. **DNA Mapping:** Converte resposta do LLM em `Archetype` do Maestro (JSON).
4. **Generation:** Alimenta o `AlbumDesigner` com esse arquétipo.

### Integration Points

* **Backend Roadmap:** @[codebase/tech/maestro_prompt/docs/backend_roadmap.md]
  * *Add:* Novo endpoint `POST /analysis/reverse-engineer`.
  * *Add:* Novo Service `MusicAnalysisService`.
* **Frontend Roadmap:** @[codebase/tech/maestro_prompt/docs/frontend_roadmap.md]
  * *Add:* Interface "DNA Decoder" (Componente Visual).
* **Task List:** @[c:\Users\t1000\.gemini\antigravity\brain\14dba9ff-b7c4-4876-9a7a-cd3f4ba567c4\task.md.resolved]
  * *Update:* Incluir tarefas da Phase 3.2 (Feature Expansion).

---

## 3. 🎨 UI/UX Experience

1. **Search Bar Hero:** Input grande e centralizado. "Paste a song link or type a name..."
2. **Scanning Animation:** Ondas sonoras, "extraindo harmonias", "detectando timbre".
3. **The DNA Dashboard:**
    * **Spectrogram Abstract:** Visualização das layers (Baixo, Bateria, Vocais).
    * **Tags Detected:** Chips interativos (e.g., "Queen-esque harmonies", "Operatic Section").
    * **Slider de "Fidelidade":**
        * *0% (Inspirado):* Vibe vaga.
        * *100% (Clone):* Mesma estrutura/bpm.
4. **Action:** "Synthesize New Batch".

---

## 4. 📅 10-Day Execution Plan

### Sprint 1: Core Logic (Days 1-4)

* **Day 1 (Spike):** Testar Prompts com LLM para ver se ele extrai dados compatíveis com `audio_specs.json` de músicas famosas.

* **Day 2 (Backend):** Criar `MusicAnalysisService` e DTO `SongDNA`.
* **Day 3 (Backend):** Implementar endpoint e integração com `MaestroTools`.
* **Day 4 (Validation):** Testes unitários do analisador. Garantir que ele não alucine gêneros fora do nosso JSON.

### Sprint 2: Frontend & Experience (Days 5-7)

* **Day 5 (Mobile/Web):** Criar componente `DNADisplay` e input de busca.

* **Day 6 (Integration):** Conectar Front ao Back. Validar fluxo de erro (música desconhecida).
* **Day 7 (Polish):** Adicionar animações de "Scanning" com Framer Motion.

### Sprint 3: Refinement & Ship (Days 8-10)

* **Day 8 (Monetization):** Implementar "Gate" (Limitar free users a 3 análises/dia).

* **Day 9 (Docs & QA):** Atualizar `walkthrough.md` e rodar E2E.
* **Day 10 (Launch):** Deploy e Demo.

---

## 5. 📚 References

* **Logic Core:** `src/application/services/album_designer.py` (será consumidor do DNA).
* **Data Source:** `data/genre_fusion_matrix.json` (Target do mapeamento).
* **Current Plan:** @[c:\Users\t1000\.gemini\antigravity\brain\14dba9ff-b7c4-4876-9a7a-cd3f4ba567c4\implementation_plan.md.resolved] -> Consultar "Phase 3.2" para encaixar esta feature.

---

> **Best Practice Recommendation:** Não tente analisar o áudio real (MP3) por enquanto. Seria lento e caro (DSP pesado). Use o "Conhecimento Latente" do LLM sobre música (Text-to-Attr) como MVP. É quase instantâneo e surpreendentemente preciso para música popular.
