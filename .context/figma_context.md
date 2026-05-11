# Figma Design Context — WF-IMS

> Reference for all frontend work. Load the relevant section per module being built — never load the full file at once.

---

## File Info

| Field | Value |
|-------|-------|
| **File name** | Werehouse |
| **Figma URL** | https://www.figma.com/design/jsEY5udLBSS9jGVykESsvk/Werehouse?node-id=0-1 |
| **File key** | `jsEY5udLBSS9jGVykESsvk` |
| **Root node** | `0:1` (Page 1) |
| **Total nodes** | 16,097 |
| **Total sections** | 14 |
| **Metadata size** | ~2.18M chars (~547K tokens) |

---

## Section Map

### MVP Sections (build these)

| Section Name | Figma Module | BP / Flow | Load Order |
|-------------|-------------|-----------|:----------:|
| `Auth` | Login & auth screens | Foundation | 1 |
| `Design System` | Colors, typography, components | Foundation | 1 |
| `Dashboard` | Main dashboard | Overview | 2 |
| `Inventory` | Stock views, lot tracking | Shared/BP-01/BP-02 | 3 |
| `Supplier` | Procurement — PR, PO, GR, vendor | BP-01 | 4 |
| `Operasional Gudang` | Goods receipt, warehouse ops | BP-01 / BP-03 | 4 |
| `Management Produksi` | Work orders, production stages | BP-02 | 5 |
| `Penjualan` | Sales orders, delivery, invoice | BP-03 | 6 |
| `Keuangan` | Payment vouchers, 3-way match | BP-01 / BP-03 | 6 |

### Phase 2 Sections (skip for MVP)

| Section Name | Reason deferred |
|-------------|-----------------|
| `QC` | QC auto-passed in MVP |
| `Analytics` | Reporting deferred |
| `Portal External` | Supplier/customer portals deferred |
| `Absensi` | Out of MVP scope entirely |
| `Pengaturan` | Settings — lower priority |

---

## Token Budget per Session

| Session | Sections to load | Est. tokens |
|---------|-----------------|:----------:|
| 1 | Auth + Design System | ~80K |
| 2 | Dashboard | ~100K |
| 3 | Inventory | ~100K |
| 4 | Supplier + Operasional Gudang | ~150K |
| 5 | Management Produksi | ~150K |
| 6 | Penjualan + Keuangan | ~200K |

**Rule: Never load more than 2 sections in one session.**

---

## How to Load a Section

Use `get_design_context` with the section's node ID. To find a section's node ID, call `get_metadata` on `0:1` and search for the section name — but do NOT do this for the full file (too large). Instead, use the node IDs below once discovered.

### Known Node IDs (fill in as discovered per session)

| Section | Node ID |
|---------|---------|
| Page 1 (root) | `0:1` |
| Portal Pelanggan | `10:9715` |
| Auth | `2:2` |
| Design System | `22:1257` |
| Design System — Color+Component overview | `14:3858` |
| Design System — Text Styles | `22:1266` |
| Design System — Sidebar component | `20:16257` |
| Design System — Navbar component | `20:16902` |
| Dashboard | TBD — load Session 2 |
| Inventory | TBD — load Session 3 |
| Supplier | TBD — load Session 4 |
| Operasional Gudang | TBD — load Session 4 |
| Management Produksi | TBD — load Session 5 |
| Penjualan | TBD — load Session 6 |
| Keuangan | TBD — load Session 6 |

> Update node IDs here as each session discovers them.

---

## Frontend Stack

| Layer | Choice |
|-------|--------|
| Framework | Flask (Python) |
| Templating | Jinja2 |
| CSS | Extract from Design System section |
| JS | Minimal — enhance Jinja2 templates only |

---

## Frontend Loading Instructions (for Claude)

When working on any frontend task for this project:

1. **Always check this file first** — find which Figma section maps to the module being built
2. **Load only the relevant section** via `get_design_context` — never the full file
3. **Extract design tokens first** (colors, spacing, typography) from Design System before building any screen
4. **Match 1:1** — implement exactly what's in Figma, do not invent UI
5. **Use Jinja2 templates** — no React/Vue, no API-only patterns

### Quick load pattern
```
Module to build → Find section in table above → get_design_context(nodeId, fileKey)
```
