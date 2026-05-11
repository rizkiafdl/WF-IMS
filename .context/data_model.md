# Data Model — WF-IMS MVP

> Flask + SQLAlchemy. All stock balances derived from transaction ledgers, never stored as a single number.

---

## Entity Relationship Overview

```
users
  └── roles: admin | manager | warehouse | production | finance

vendors ──────────────────┐
materials ─── bom_items   │
  │                       │
  └── lot_transactions    │
        ▲                 │
        │              purchase_orders ──── purchase_requisitions
goods_receipts ──────────┘       │
  │                              └── supplier_invoices ── payment_vouchers
  └── rm_lots
        │
        └── wo_lot_allocations ─── work_orders
                                        │
                                   fg_batches ── lot_transactions
                                        │
                                   so_line_items ─── sales_orders ── customers
                                        │                 │
                                   delivery_orders    invoices ── receipt_vouchers
```

---

## Tables

### Foundation

```sql
-- users
id, email, password_hash, full_name, role (enum: admin|manager|warehouse|production|finance), is_active, created_at

-- vendors
id, name, contact_name, phone, email, address, payment_terms (int days), is_active, created_at

-- customers
id, name, contact_name, phone, email, address, payment_terms (int days), is_active, created_at

-- materials
id, name, unit (kg|ton|bag), reorder_point (decimal), material_type (enum: raw_material|finished_goods), created_at

-- bom_items  (1 finished good → many raw materials)
id, fg_material_id (FK materials), rm_material_id (FK materials), qty_per_unit (decimal)
```

---

### BP-01 Procurement

```sql
-- purchase_requisitions
id, pr_number (auto: PR-YYYYMMDD-NNN), material_id (FK), qty (decimal), unit, reason,
status (enum: draft|submitted|approved|rejected), requested_by (FK users),
approved_by (FK users nullable), approved_at, created_at

-- purchase_orders
id, po_number (auto: PO-YYYYMMDD-NNN), pr_id (FK nullable), vendor_id (FK),
material_id (FK), qty_ordered (decimal), unit_price (decimal), total_amount (decimal),
expected_delivery_date, status (enum: draft|sent|confirmed|received|closed|cancelled),
confirmed_at, created_by (FK users), created_at

-- goods_receipts
id, gr_number (auto: GR-YYYYMMDD-NNN), po_id (FK),
gross_weight (decimal), tare_weight (decimal), net_weight (decimal),
weight_variance_pct (computed), is_within_tolerance (bool),
received_by (FK users), received_at, notes

-- rm_lots
id, lot_id (auto: LOT-YYYYMMDD-NNN), gr_id (FK), material_id (FK),
qty (decimal), unit, status (enum: available|locked|consumed|returned),
putaway_location (string, default 'RM-WAREHOUSE'), created_at

-- supplier_invoices
id, invoice_number (supplier's own number), po_id (FK), vendor_id (FK),
invoice_amount (decimal), invoice_date, received_date,
match_status (enum: pending|matched|exception), matched_at,
created_by (FK users), created_at

-- payment_vouchers
id, voucher_number (auto: PV-YYYYMMDD-NNN), invoice_id (FK),
amount (decimal), payment_method (string), payment_date,
journal_entry (json: {debit: 'AP', credit: 'Bank', amount: x}),
created_by (FK users), paid_at
```

---

### BP-02 Production

```sql
-- work_orders
id, wo_number (auto: WO-YYYYMMDD-NNN), fg_material_id (FK materials),
target_qty (decimal), unit,
status (enum: draft|submitted|approved|rejected|in_progress|production_complete|completed),
approved_by (FK users nullable), approved_at,
created_by (FK users), started_at, completed_at, created_at

-- wo_production_stages
id, wo_id (FK), stage_number (1-6),
stage_name (chipping|drying|pelleting|cooling|screening|packing),
status (enum: pending|done), done_by (FK users nullable), done_at

-- wo_lot_allocations
id, wo_id (FK), rm_lot_id (FK rm_lots),
qty_allocated (decimal), qty_consumed (decimal nullable)

-- fg_batches
id, batch_id (auto: BATCH-YYYYMMDD-NNN), wo_id (FK), material_id (FK),
qty (decimal), unit,
status (enum: available|reserved|shipped|consumed),
produced_at, created_at
```

---

### BP-03 Sales

```sql
-- sales_orders
id, so_number (auto: SO-YYYYMMDD-NNN), customer_id (FK),
status (enum: draft|submitted|approved|rejected|picking|shipped|delivered|invoiced|paid|cancelled),
approved_by (FK users nullable), approved_at,
created_by (FK users), created_at, notes

-- so_line_items
id, so_id (FK), material_id (FK), qty_ordered (decimal), unit_price (decimal),
batch_id (FK fg_batches nullable, assigned at picking), qty_picked (decimal nullable)

-- delivery_orders
id, do_number (auto: DO-YYYYMMDD-NNN), so_id (FK),
driver_name, vehicle_plate, shipped_at, delivered_at,
status (enum: pending|shipped|delivered),
created_by (FK users)

-- invoices
id, invoice_number (auto: INV-YYYYMMDD-NNN), so_id (FK), customer_id (FK),
amount (decimal), due_date,
status (enum: draft|sent|paid|overdue),
journal_entry (json: {debit: 'AR', credit: 'Revenue', amount: x}),
sent_at, paid_at, created_by (FK users), created_at

-- receipt_vouchers
id, voucher_number (auto: RV-YYYYMMDD-NNN), invoice_id (FK),
amount (decimal), payment_method (string), payment_date,
journal_entry (json: {debit: 'Bank', credit: 'AR', amount: x}),
created_by (FK users), created_at
```

---

### Shared: Inventory Ledger

```sql
-- stock_transactions  (THE central ledger — never update qty directly)
id, transaction_type (enum: gr_in|wo_consume|wo_produce|so_ship|adjustment),
material_id (FK), lot_id (string, rm lot or fg batch id),
qty_change (decimal, positive = IN, negative = OUT),
reference_type (string: GoodsReceipt|WorkOrder|SalesOrder),
reference_id (int), notes,
created_by (FK users), created_at
```

**Stock balance query (always derive, never cache):**
```sql
SELECT material_id, SUM(qty_change) as current_stock
FROM stock_transactions
WHERE material_id = :id
GROUP BY material_id
```

---

## Key Design Decisions

1. **Stock as ledger** — `stock_transactions` is append-only. Current balance = SUM. Never store qty on `materials` table.
2. **Auto-numbering** — All document numbers (PR-YYYYMMDD-NNN) generated in Flask, not in DB.
3. **Journal entries as JSON** — Stored on voucher rows for MVP. Not a full double-entry ledger.
4. **Lot ID vs Batch ID** — RM uses `lot_id` (from GR), FG uses `batch_id` (from WO). Same concept, separate naming for clarity.
5. **FIFO** — Enforced by ordering `rm_lots` / `fg_batches` by `created_at ASC` when allocating.