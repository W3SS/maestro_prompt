# Phase 3: Frontend Implementation Plan - Maestro AI Workstation

## 📋 Overview

**Goal:** Build a modern, professional React SPA for Maestro AI that provides an intuitive interface for album generation and batch management.

**Target Users:** Music producers, artists, content creators using Suno AI.

**Core Value Proposition:** Streamline album conceptualization and batch processing with AI-powered design tools.

---

## 🎨 Design Philosophy

### Visual Identity

**Color Palette (Dark Mode First):**

- Primary: `#6366f1` (Indigo) - Creative energy
- Secondary: `#8b5cf6` (Purple) - Musical innovation
- Accent: `#ec4899` (Pink) - AI-powered magic
- Success: `#10b981` (Green)
- Warning: `#f59e0b` (Amber)
- Error: `#ef4444` (Red)
- Background: `#0f172a` (Slate 900)
- Surface: `#1e293b` (Slate 800)
- Text: `#f1f5f9` (Slate 100)

**Typography:**

- Headings: `Inter` (bold, 600-700 weight)
- Body: `Inter` (regular, 400-500 weight)
- Code/Mono: `Fira Code` (for JSON/outputs)

**Design Principles:**

1. **Immersive**: Full-screen layouts with minimal chrome
2. **Responsive**: Desktop-first, mobile-aware
3. **Accessible**: WCAG 2.1 AA compliant
4. **Animated**: Micro-interactions for feedback
5. **Modular**: Component-driven architecture

---

## 🏗️ Technical Stack

### Core Framework

```json
{
  "framework": "React 18+",
  "build_tool": "Vite",
  "language": "TypeScript",
  "styling": "TailwindCSS v4",
  "state": "Zustand",
  "routing": "React Router v6",
  "forms": "React Hook Form + Zod",
  "http": "Axios",
  "ui_kit": "Radix UI (headless)",
  "animations": "Framer Motion",
  "icons": "Lucide React"
}
```

### Why This Stack?

- **Vite:** Lightning-fast dev server, 10x faster than CRA
- **Zustand:** Simpler than Redux, type-safe, minimal boilerplate  
- **TailwindCSS v4:** Utility-first, CSS-in-TS, zero runtime
- **Radix UI:** Accessible primitives, fully customizable
- **Framer Motion:** Declarative animations, smooth gestures

---

## 📐 Application Architecture

### File Structure

```
frontend/
├── public/
│   ├── favicon.svg
│   └── og-image.png
├── src/
│   ├── app/               # App shell
│   │   ├── App.tsx
│   │   ├── router.tsx
│   │   └── providers.tsx
│   ├── features/          # Feature modules
│   │   ├── album-designer/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── store.ts
│   │   │   └── types.ts
│   │   ├── batch-manager/
│   │   └── dashboard/
│   ├── shared/            # Shared utilities
│   │   ├── components/    # Reusable UI
│   │   ├── hooks/
│   │   ├── lib/           # API client, utils
│   │   └── types/
│   ├── styles/
│   │   ├── globals.css
│   │   └── theme.ts
│   └── main.tsx
├── tests/
│   ├── unit/
│   └── e2e/
├── package.json
├── vite.config.ts
├── tailwind.config.ts
└── tsconfig.json
```

### State Management Pattern

```typescript
// Zustand store structure
interface AlbumStore {
  // State
  currentAlbum: Album | null;
  isGenerating: boolean;
  
  // Actions
  designAlbum: (input: DesignInput) => Promise<Album>;
  reset: () => void;
}

interface BatchStore {
  batches: Batch[];
  activeBatch: string | null;
  
  fetchBatches: (filter?: string) => Promise<void>;
  createBatch: (name: string) => Promise<Batch>;
  addTrackToBatch: (batchId: string, track: Track) => Promise<void>;
}
```

---

## 🎯 Core Features

### Feature 1: Album Designer 🎨

**Purpose:** Generate concept albums with AI using archetype + genres.

**UI Components:**

1. **Input Panel** (left sidebar, 30% width)

   ```
   ┌──────────────────┐
   │ 🎭 Archetype     │
   │ [Dropdown v]     │
   │                  │
   │ 🎸 Genres        │
   │ [Multi-select]   │
   │                  │
   │ 🎵 # Tracks      │
   │ [Slider 1-20]    │
   │                  │
   │ [✨ Generate]    │
   └──────────────────┘
   ```

2. **Output Panel** (right, 70% width)

   ```
   ┌────────────────────────────┐
   │ Album: "Cyberpunk Dreams"  │
   │                            │
   │ Track 1: Neon Horizon      │
   │ ├─ Lyrics: [Preview...]   │
   │ ├─ Style: Dark Synthwave   │
   │ └─ Duration: 3:42         │
   │                            │
   │ [+ Add to Batch]   [Copy]│
   └────────────────────────────┘
   ```

**Interactions:**

- Real-time validation (archetype required)
- Loading skeleton during generation (~5-10s)
- **Copy to clipboard** button for each track
- **Add to batch** CTA with batch selector modal

**API Integration:**

```typescript
POST /album/design
{
  "archetype": "Cosmic Wanderer",
  "genres": ["Synthwave", "Ambient"],
  "num_tracks": 8
}
→ Response: { "title": "...", "tracks": [...] }
```

---

### Feature 2: Batch Manager 📦

**Purpose:** Organize tracks into batches for Suno processing.

**UI Layout:**

1. **Batch List** (left, 35%)

   ```
   ┌─────────────────┐
   │ [+ New Batch]   │
   │                 │
   │ ● Summer 2024   │
   │   12 tracks     │
   │                 │
   │ ● EP Release    │
   │   3 tracks      │
   └─────────────────┘
   ```

2. **Batch Detail** (right, 65%)

   ```
   ┌───────────────────────────┐
   │ Summer 2024  [⚙️ Actions]│
   │ Status: ● PENDING         │
   │                           │
   │ 🎵 Track 1: Title         │
   │ 🎵 Track 2: Title         │
   │                           │
   │ [▶ Start] [✓ Complete]    │
   └───────────────────────────┘
   ```

**Actions Menu:**

- Start Batch
- Complete Batch
- Cancel Batch
- Export JSON (download)

**Status Badges:**

- `PENDING` → Yellow pulse  
- `PROCESSING` → Blue spinner  
- `COMPLETED` → Green check  
- `CANCELLED` → Red X  

**API Integration:**

```typescript
GET /batches?status=PENDING
POST /batch
POST /batch/{id}/items
POST /batch/{id}/start
```

---

### Feature 3: Dashboard 📊 (Future)

**Purpose:** Real-time stats and workflow overview.

**Widgets:**

- Total albums generated
- Active batches
- Recent activity timeline

---

## 🧩 Component Library

### Shared Components

1. **`<Card />`** - Container with glass morphism

   ```tsx
   <Card variant="glass" padding="lg">
     <CardHeader title="Album Designer" />
     <CardContent>{children}</CardContent>
   </Card>
   ```

2. **`<Button />`** - Primary, secondary, ghost variants

   ```tsx
   <Button 
     variant="primary" 
     size="lg" 
     icon={<Sparkles />}
     loading={isGenerating}
   >
     Generate Album
   </Button>
   ```

3. **`<Select />`** - Custom dropdown with Radix
4. **`<MultiSelect />`** - Checkbox-based genre picker
5. **`<Slider />`** - Range input for track count
6. **`<Badge />`** - Status indicators
7. **`<Modal />`** - Overlay for batch selection
8. **`<Toast />`** - Success/error notifications

---

## 🎬 Animations & Interactions

**Micro-animations:**

- **Card hover:** Subtle elevation + glow effect
- **Button:** Scale (0.95) on click
- **Generate:** Shimmer effect during loading
- **Track reveal:** Stagger animation (50ms delay each)

**Framer Motion Example:**

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  {track.title}
</motion.div>
```

---

## ✅ Testing Strategy

### Unit Tests (Vitest + React Testing Library)

- All shared components (>90% coverage)
- Store actions (Zustand)
- Utility functions

### Integration Tests

- Album generation flow (E2E)
- Batch CRUD operations

### Accessibility Tests

- aria-labels on all interactive elements
- Keyboard navigation (Tab, Enter, Esc)
- Screen reader compatibility (axe-core)

---

## 📥 Phase Breakdown

### Phase 3.1: Foundation (Week 1)

- [ ] Vite + React + TypeScript setup
- [ ] TailwindCSS v4 + theme configuration
- [ ] API client (`axios` + base URL)
- [ ] Routing (`/`, `/album`, `/batches`)
- [ ] Zustand stores (skeleton)

### Phase 3.2: Album Designer (Week 2)

- [ ] Input form with validation (Zod)
- [ ] API integration (`POST /album/design`)
- [ ] Track list display with copy CTA
- [ ] Add to batch modal
- [ ] Loading states + error handling

### Phase 3.3: Batch Manager (Week 3)

- [ ] Batch list (fetch + display)
- [ ] Batch detail view
- [ ] CRUD actions (create, add items, start, complete)
- [ ] Status indicators with real-time updates

### Phase 3.4: Polish (Week 4)

- [ ] Animations (Framer Motion)
- [ ] Accessibility audit (axe DevTools)
- [ ] Responsive design (mobile breakpoints)
- [ ] E2E tests (Playwright)
- [ ] Performance optimization (Lighthouse >90)

---

## 🚀 Deployment

**Production Build:**

```bash
npm run build
# → dist/ (static files)
```

**Hosting Options:**

- Vercel (recommended, zero-config)
- Netlify
- Cloudflare Pages

**Environment Variables:**

```
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Maestro AI
```

---

## 📊 Success Metrics

**Technical:**

- Lighthouse score >90 (Performance, Accessibility, SEO)
- First Contentful Paint <1.5s
- Test coverage >90%

**UX:**

- Album generation <10s (backend dependent)
- Zero-click batch selection (smart defaults)
- Keyboard shortcuts for power users

---

## Next Steps

1. Get user approval on design direction
2. Create high-fidelity mockups (Figma/code)
3. Implement Phase 3.1 (Foundation)
4. Iterate with user feedback
