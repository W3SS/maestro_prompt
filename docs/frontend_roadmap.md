# Frontend Implementation Roadmap (Phase 3)

> **Goal:** Build a professional, immersive React application for Maestro AI that integrates with the existing FastAPI/MCP backend.

## 🎨 Visual Identity

- **Theme:** Dark Mode First
- **Palette:**
  - Primary: Indigo (`#6366f1`)
  - Secondary: Purple (`#8b5cf6`)
  - Background: Slate 900 (`#0f172a`)
- **Typography:** Inter (Headings/Body), Fira Code (Mono)

## 📅 Phases & Tasks

### Phase 3.1: Foundation (Current)

- [x] **Project Init**: Scaffold with Vite + React + TS (`src/presentation/web`).
- [x] **Styling**: Configure TailwindCSS v4 with custom theme tokens (Dependencies Installed).
- [x] **Routing**: Setup React Router v6 (Dependencies Installed).
- [x] **State**: Initialize Zustand stores (Dependencies Installed).
- [x] **API**: Setup Axios instance (Dependencies Installed).

> **Note:** Switched to `yarn` for package management due to filesystem locking issues.

### Phase 3.2: Album Designer

- [ ] **Layout**: Two-panel design (Inputs vs Output).
- [ ] **Components**:
  - `GenerateForm` (RHF + Zod)
  - `TrackList` (with animation)
  - `AlbumCard`
- [ ] **Feature: Song DNA Decoder**:
  - [ ] Search Input (Song/Artist)
  - [ ] Visualization: "Scanning" Animation (Framer Motion)
  - [ ] Dashboard: Spectrogram + Tag Chips + Fidelity Slider
- [ ] **Integration**: Connect to `POST /album/design` and `POST /analysis/reverse-engineer`.

### Phase 3.3: Batch Manager

- [ ] **Layout**: Dashboard style with Sidebar list.
- [ ] **Components**:
  - `BatchList` (Virtual scroll if needed)
  - `BatchStatusBadge` (Animated)
  - `ControlBar` (Start/Stop/Cancel)
- [ ] **Integration**: Connect to Batch APIs (Poling or WebSocket).

### Phase 3.4: Polish & Deploy

- [ ] **Micro-animations**: Framer Motion for transitions.
- [ ] **Accessibility**: Audit with axe-core.
- [ ] **Build**: PM2 or Docker setup for serving static files.

## 📂 Proposed Structure

```
src/presentation/web/
├── public/
├── src/
│   ├── app/                # Providers, Router, Entry
│   ├── components/         # Shared UI (Button, Input, Card)
│   ├── features/           # Feature-based modules
│   │   ├── album-designer/
│   │   └── batch-manager/
│   ├── hooks/              # Shared hooks
│   ├── lib/                # Utils, API client, Zod schemas
│   ├── stores/             # Zustand stores
│   └── styles/             # Global CSS, Tailwind config
```
