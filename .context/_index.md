# WF-IMS — Context Index

> **Project:** Wood Fuel Integrated Management System
> **Type:** ERP for wood pellet manufacturing company
> **Stack:** Python / Flask + Jinja2 templates + SQLAlchemy
> **Phase:** MVP planning — pre-code

---

## Project in One Paragraph

WF-IMS is an ERP system for a company that buys raw wood, manufactures wood pellets through a 6-stage production process, and sells the finished pellets to buyers. The system covers three core flows end-to-end: **Procurement** (buy raw materials from suppliers), **Production** (turn raw materials into pellets), and **Sales** (sell pellets and collect payment). Inventory is the shared ledger connecting all three flows.

---

## Current Status

| Phase | Status |
|-------|--------|
| Business process documentation | ✅ Done |
| MVP scope definition | ✅ Done |
| Data model design | ✅ Done |
| User roles & permissions | ✅ Done |
| Flask project scaffolding | ⬜ Not started |
| Database migrations | ⬜ Not started |
| UI / screens | ⬜ Not started |

---

## Document Index

### Business Process Docs

| File | Description | Use when |
|------|-------------|----------|
| `lms.md` | **Full** business process (8 BPs, original version with QC) | Understanding the complete system, Phase 2 planning |
| `bp_01_06.md` | BP-01 Procurement + BP-06 Inventory — detailed/extended version with QC, moisture routing, scorecard | Phase 2 reference |
| `bp_01_simplified.md` | **BP-01 Procurement — MVP version** (QC removed, single warehouse) | Building procurement module |
| `bp_02_simplified.md` | **BP-02 Production — MVP version** (auto-pass QC, 6-stage checklist) | Building production module |
| `bp_03_simplified.md` | **BP-03 Sales — MVP version** (no credit check, no customer portal) | Building sales module |

### Engineering Docs

| File | Description | Use when |
|------|-------------|----------|
| `mvp_scope.md` | **Single source of truth** — what is IN and OUT of MVP | Deciding whether to build a feature |
| `data_model.md` | All database tables across 3 BPs, SQLAlchemy-ready | Writing models, migrations |
| `user_roles.md` | Role/permission matrix + Flask decorator pattern | Writing route auth, building UI nav |
| `figma_context.md` | Figma file map, 14 sections, node IDs, token budget per session | Any frontend / UI work |
| `frontend_style_guide.md` | **Complete CSS guideline** — colors, typography, buttons, layout, tables | Before writing any HTML/CSS |

### Development Docs

| File | Description | Use when |
|------|-------------|----------|
| `development/implementation_plan.md` | **Full build plan** — all 12 phases, every file, every route, all business logic | Before/during execution |
| `development/progress.md` | Live phase tracker — what's done, issues, deferred items | During execution |

### Notes

| File | Description |
|------|-------------|
| `catatan.md` | Actor definitions and key term glossary |
| `_index.md` | This file — project overview and document index |

---

## Key Decisions (Already Made)

| Decision | Choice | Reason |
|----------|--------|--------|
| Tech stack | Flask + Jinja2 + SQLAlchemy | User preference |
| QC in MVP | Auto-pass (skipped) | Deferred to Phase 2 |
| Stock model | Transaction ledger (`stock_transactions`) not a single qty field | Correct ERP pattern, audit trail |
| Lot ID | Generated at Goods Receipt | No QC gate in MVP |
| 3 core flows | Procurement + Production + Sales | Proven end-to-end loop for demo |
| FIFO | Enforced on both RM lot allocation and FG batch picking | Business rule from lms.md |
| Counter-offer / negotiation | Out of MVP | Too complex for demo |
| Return-to-Supplier | Out of MVP | Rare without QC gate |
| Credit limit check | Out of MVP | No finance master data yet |

---

## Key Concepts Glossary

| Term | Meaning |
|------|---------|
| **P2P** | Procure-to-Pay — procurement to supplier payment |
| **MRP** | Material Requirements Planning — production planning |
| **O2C** | Order-to-Cash — sales order to customer payment |
| **PR** | Purchase Requisition |
| **PO** | Purchase Order |
| **GR / GRN** | Goods Receipt / Goods Receipt Note |
| **WO** | Work Order |
| **SO** | Sales Order |
| **DO** | Delivery Order (Surat Jalan) |
| **BOM** | Bill of Materials |
| **Lot ID** | Unique ID for a batch of raw material received |
| **Batch ID** | Unique ID for a batch of finished goods produced |
| **CoA** | Certificate of Analysis — QC result document (Phase 2) |
| **HPP** | Harga Pokok Produksi — cost of goods produced (Phase 2) |
| **ROP** | Reorder Point — stock level that triggers a new PR |
| **FIFO** | First In First Out — oldest stock used/sold first |
| **3-Way Match** | PO + GRN + Invoice must agree before payment |
| **AP** | Accounts Payable — money owed to suppliers |
| **AR** | Accounts Receivable — money owed by customers |

---

## Demo Flow (10 min walk-through)

```
1. PROCUREMENT
   Stock ≤ ROP → Create PR → Manager approves → Create PO
   → Supplier confirms → Warehouse receives (GR + weight check)
   → Lot ID generated → Finance: 3-Way Match → Payment Voucher → Paid
   ✓ RM Lot now in inventory (Available)

2. PRODUCTION
   Create Work Order → System shows FIFO lots → Manager approves
   → Lots locked → Staff checks off 6 stages (Chipping→Packing)
   → Mark Production Complete → Auto-pass QC
   → FG Batch ID generated → RM stock decremented → FG stock added
   ✓ FG Batch now in inventory (Available)

3. SALES
   Admin creates SO → Manager approves → Warehouse picks FG batches (FIFO)
   → Generate Surat Jalan → Mark Shipped → Confirm delivery
   → Finance generates Invoice → Customer pays → Receipt Voucher → Paid
   ✓ SO Closed, FG stock decremented, AR cleared
```

---

## What to Read First (for a new session)

1. `_index.md` — this file (overview)
2. `mvp_scope.md` — what's in/out
3. `data_model.md` — tables and relationships
4. The relevant simplified BP file for the module being built
