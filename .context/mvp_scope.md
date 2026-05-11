# MVP Scope — WF-IMS

> Single source of truth for what is IN and OUT of MVP across all 3 business processes.

---

## In Scope (Build This)

### Foundation
- [x] User auth (login/logout, role-based)
- [x] Vendor Master (CRUD)
- [x] Customer Master (CRUD)
- [x] Material Master (CRUD, with ROP field)
- [x] BOM (Bill of Materials) per material

### BP-01 — Procurement
- [x] Purchase Requisition — create, submit, approve/reject
- [x] Purchase Order — create from PR, send, confirm
- [x] Goods Receipt — input weights, auto Lot ID, putaway
- [x] Supplier Invoice input
- [x] 3-Way Match (PO vs GR vs Invoice)
- [x] Payment Voucher — create, mark paid
- [x] Journal entry display (DR AP / CR Bank)

### BP-02 — Production
- [x] Work Order — create, approve/reject
- [x] FIFO lot suggestion for RM allocation
- [x] Lot lock on WO approval
- [x] 6-stage production checklist (checkbox per stage)
- [x] Auto-pass QC on completion
- [x] FG Batch ID generation
- [x] RM stock decrement + FG stock increment on WO complete

### BP-03 — Sales
- [x] Sales Order — create (Admin), approve/reject (Manager)
- [x] FG batch reservation (FIFO) on SO approval
- [x] Picking confirmation by Warehouse Staff
- [x] Delivery Order (Surat Jalan) generation
- [x] Shipment + delivery confirmation
- [x] Invoice generation
- [x] Receipt Voucher — create, mark paid
- [x] Journal entry display (DR Bank / CR AR)

### Inventory (shared)
- [x] RM lot ledger (IN from GR, OUT from WO)
- [x] FG batch ledger (IN from WO complete, OUT from SO shipment)
- [x] Real-time stock balance per material (sum of transactions)
- [x] Low stock alert (stock ≤ ROP)

---

## Out of Scope (Phase 2)

### Quality Control
- [ ] QC inspection (8 ENplus parameters)
- [ ] Rework flow
- [ ] Scrap flow
- [ ] CoA (Certificate of Analysis) generation
- [ ] Quarantine location

### Procurement
- [ ] Budget check before PR
- [ ] Supplier counter-offer / negotiation
- [ ] Return-to-Supplier flow
- [ ] Partial goods receipt
- [ ] Supplier Scorecard
- [ ] Supplier self-service portal

### Production
- [ ] HPP (cost of production) tracking per stage
- [ ] Waste / yield recording
- [ ] Stage-level detail input (temperatures, BBM, etc.)

### Sales
- [ ] Credit limit check
- [ ] Auto payment reminders
- [ ] Customer self-service portal
- [ ] Return / refund flow
- [ ] Partial delivery

### Finance
- [ ] Full general ledger
- [ ] Chart of accounts management
- [ ] Monthly financial close
- [ ] P&L / Balance Sheet reports
- [ ] Bank reconciliation

### Analytics
- [ ] Dashboards and trend reports

---

## Demo Script (10-minute walk-through)

1. **Procurement** — Stock drops below ROP → create PR → Manager approves → create PO → supplier confirms → warehouse receives goods (GR) → 3-Way Match → pay supplier → RM Lot now in stock
2. **Production** — Create Work Order → system shows FIFO lots → Manager approves → staff checks off 6 stages → WO complete → FG Batch in stock
3. **Sales** — Admin creates SO → Manager approves → warehouse picks FG batches → generate Surat Jalan → mark shipped → confirm delivery → generate Invoice → mark paid

Total screens walked: ~12. Total flow time: ~10 min.
