# WF-IMS — Claude Code Instructions

> Wood Fuel Integrated Management System
> ERP for wood pellet manufacturing: Procurement → Production → Sales
> Stack: Python / Flask + Jinja2 + SQLAlchemy + SQLite

---

## 1. Startup — What to Read First

**Every session, always load in this order:**

1. `.context/_index.md` — project overview + full document index
2. `.context/development/progress.md` — current build phase, what's done, open issues

Then load task-specific files based on what you're working on (see section 3).

---

## 2. Context Folder Map

```
.context/
│
├── _index.md                         ← master index, read every session
│
├── development/                      ← active build tracking
│   ├── implementation_plan.md        ← full 12-phase build plan, all routes & models
│   └── progress.md                   ← live phase tracker, issues, deferred items
│
├── mvp_scope.md                      ← IN/OUT of MVP (source of truth for scope)
├── data_model.md                     ← all SQLAlchemy models, table fields, relationships
├── user_roles.md                     ← role/permission matrix + Flask decorator pattern
│
├── frontend_style_guide.md           ← CSS tokens, typography, colors, components
├── figma_context.md                  ← Figma file map, section node IDs, token budget
│
├── bp_01_simplified.md               ← Procurement flow MVP
├── bp_02_simplified.md               ← Production flow MVP
├── bp_03_simplified.md               ← Sales flow MVP
│
├── lms.md                            ← full original 8-BP business process (Phase 2 ref)
├── bp_01_06.md                       ← extended BP-01 + BP-06 with QC (Phase 2 ref)
└── catatan.md                        ← actor definitions + glossary
```

---

## 3. Task-Based Context Loading

Load only what the task needs. Do not load all files every session.

| Task type | Load these files |
|-----------|-----------------|
| **Any task** | `_index.md` + `development/progress.md` |
| **Backend / models** | + `data_model.md` |
| **Procurement feature** | + `bp_01_simplified.md` + `data_model.md` |
| **Production feature** | + `bp_02_simplified.md` + `data_model.md` |
| **Sales feature** | + `bp_03_simplified.md` + `data_model.md` |
| **Auth / permissions** | + `user_roles.md` |
| **Any frontend / HTML / CSS** | + `frontend_style_guide.md` + `figma_context.md` |
| **Figma screen implementation** | + `frontend_style_guide.md` + `figma_context.md` → load `figma:figma-implement-design` skill |
| **Scope decision** | + `mvp_scope.md` |
| **Phase 2 planning** | + `lms.md` + `bp_01_06.md` |

---

## 4. Build State

- **Current phase**: See `development/progress.md`
- **Plan**: `development/implementation_plan.md` — 12 phases, ~65 files
- **Root dir**: `/Users/muhammadrizkiafdolli/rizkiafdl/project-lms/`
- **DB**: SQLite — `wfims.db` at project root
- **Entry point**: `run.py` → `flask run`

After every phase completes, update `development/progress.md` — mark phase ✅, log any issues or deviations.

---

## 5. Coding Rules

### General
- Flask app factory pattern — `create_app()` in `app/__init__.py`
- One blueprint per module: `auth`, `dashboard`, `master`, `procurement`, `production`, `sales`, `inventory`
- Never store stock as a single qty field — always write a `StockTransaction` row
- Document numbers are auto-generated in Flask (not in DB): `PR-YYYYMMDD-NNN`, `WO-YYYYMMDD-NNN`, etc.

### Models
- All models import `db` from `app/extensions.py`
- SQLite: add `PRAGMA foreign_keys=ON` on connect
- Use `db.Enum` for status fields — never raw strings

### Templates
- Always extend `base.html`
- Use `{% include 'partials/navbar.html' %}` and `{% include 'partials/sidebar.html' %}`
- No inline styles — all styling via CSS classes from `frontend_style_guide.md`

### CSS
- All color/size values must reference CSS custom properties from `tokens.css`
- No hardcoded hex values in templates or component CSS

### Business Logic
- FIFO: `order_by(created_at.asc())`
- Lot lock on WO approve: set `RMLot.status = 'locked'`
- Stock writes happen at: GR save, WO complete, SO shipment — nowhere else

---

## 6. Frontend / Figma Rules

- **Figma file key**: `jsEY5udLBSS9jGVykESsvk` — 16,097 nodes, 14 sections
- Never call `get_design_context` on the root node (`0:1`) — always use section-level node IDs
- Max 2 Figma sections per session (token budget)
- Known section node IDs are in `figma_context.md` — update the file when new ones are discovered
- Load `figma:figma-implement-design` skill before implementing any Figma screen

---

## 7. What to Save to .context/

| Save here | Don't save here |
|-----------|----------------|
| Architecture decisions | Code snippets (live in codebase) |
| Scope changes (update `mvp_scope.md`) | Temporary task state |
| New Figma node IDs (update `figma_context.md`) | Anything already in git history |
| Build issues/deviations (update `progress.md`) | Anything derivable from reading the code |
| Business rule clarifications from user | |
