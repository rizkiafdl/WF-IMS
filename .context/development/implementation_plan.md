# WF-IMS MVP — Implementation Plan

> **Root directory**: `/Users/muhammadrizkiafdolli/rizkiafdl/project-lms/`
> **Stack**: Python / Flask + Jinja2 + SQLAlchemy + SQLite
> **Status**: Pre-execution — plan only

---

## Execution Phases

```
Phase 1 → Foundation          (config, requirements, app factory, extensions)
Phase 2 → Database Models     (all SQLAlchemy models)
Phase 3 → CSS Design System   (tokens → base → layout → components)
Phase 4 → Base Templates      (base.html, navbar, sidebar)
Phase 5 → Auth Module         (login, logout, role guard)
Phase 6 → Dashboard Module    (home, summary cards)
Phase 7 → Master Data Module  (vendor, customer, material, BOM)
Phase 8 → Procurement Module  (PR → PO → GR → Invoice → Payment)
Phase 9 → Production Module   (WO → stages → FG batch)
Phase 10 → Sales Module       (SO → pick → deliver → invoice → paid)
Phase 11 → Inventory Module   (stock ledger, lot view)
Phase 12 → Wire-up & Verify   (flask run, db init, smoke test)
```

---

## Full File Tree (target state)

```
project-lms/
│
├── CLAUDE.md
├── run.py
├── config.py
├── requirements.txt
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── master.py
│   │   ├── procurement.py
│   │   ├── production.py
│   │   ├── sales.py
│   │   └── inventory.py
│   │
│   ├── blueprints/
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── dashboard/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── master/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── procurement/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── production/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── sales/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   └── inventory/
│   │       ├── __init__.py
│   │       └── routes.py
│   │
│   └── templates/
│       ├── base.html
│       ├── partials/
│       │   ├── navbar.html
│       │   └── sidebar.html
│       ├── auth/
│       │   └── login.html
│       ├── dashboard/
│       │   └── index.html
│       ├── master/
│       │   ├── vendors.html
│       │   ├── vendor_form.html
│       │   ├── customers.html
│       │   ├── customer_form.html
│       │   ├── materials.html
│       │   └── material_form.html
│       ├── procurement/
│       │   ├── pr_list.html
│       │   ├── pr_form.html
│       │   ├── pr_detail.html
│       │   ├── po_list.html
│       │   ├── po_form.html
│       │   ├── po_detail.html
│       │   ├── gr_list.html
│       │   ├── gr_form.html
│       │   ├── invoice_list.html
│       │   ├── invoice_form.html
│       │   └── payment_list.html
│       ├── production/
│       │   ├── wo_list.html
│       │   ├── wo_form.html
│       │   └── wo_detail.html
│       ├── sales/
│       │   ├── so_list.html
│       │   ├── so_form.html
│       │   ├── so_detail.html
│       │   ├── delivery_list.html
│       │   ├── delivery_form.html
│       │   ├── invoice_list.html
│       │   ├── invoice_form.html
│       │   └── payment_list.html
│       └── inventory/
│           ├── stock.html
│           └── lot_detail.html
│
├── static/
│   ├── css/
│   │   ├── tokens.css
│   │   ├── base.css
│   │   ├── layout.css
│   │   ├── components.css
│   │   └── main.css
│   └── js/
│       └── main.js
│
├── migrations/
│
└── .context/
    ├── _index.md
    ├── development/
    │   ├── implementation_plan.md     ← this file
    │   └── progress.md               ← updated as each phase completes
    └── ...
```

**Total files to create**: ~65

---

## Phase Detail

### Phase 1 — Foundation

| File | Purpose |
|------|---------|
| `requirements.txt` | Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate, Werkzeug |
| `config.py` | DevelopmentConfig with SQLite URI, secret key, debug flag |
| `run.py` | Entry point — `create_app()` + `app.run()` |
| `app/__init__.py` | App factory `create_app()`, register blueprints, init extensions |
| `app/extensions.py` | `db`, `login_manager`, `migrate` instances |

**Key decisions:**
- DB: `sqlite:///wfims.db` (file created at project root)
- SQLite foreign key enforcement via `PRAGMA foreign_keys=ON` on connect
- Secret key from env var with fallback for dev

---

### Phase 2 — Database Models

All models live in `app/models/`. Every file imports from `app/extensions.py`.

#### `user.py`
```
User: id, email, password_hash, full_name, role (enum), is_active, created_at
Role enum: admin | manager | warehouse | production | finance
```

#### `master.py`
```
Vendor:   id, name, contact_name, phone, email, address, payment_terms, is_active
Customer: id, name, contact_name, phone, email, address, payment_terms, is_active
Material: id, name, unit, reorder_point, material_type (raw_material | finished_goods)
BOMItem:  id, fg_material_id → Material, rm_material_id → Material, qty_per_unit
```

#### `procurement.py`
```
PurchaseRequisition: id, pr_number, material_id, qty, unit, reason,
                     status (draft|submitted|approved|rejected),
                     requested_by, approved_by, approved_at, created_at

PurchaseOrder: id, po_number, pr_id, vendor_id, material_id,
               qty_ordered, unit_price, total_amount, expected_delivery_date,
               status (draft|sent|confirmed|received|closed|cancelled),
               created_by, created_at

GoodsReceipt: id, gr_number, po_id, gross_weight, tare_weight, net_weight,
              weight_variance_pct, is_within_tolerance,
              received_by, received_at, notes

RMLot: id, lot_id, gr_id, material_id, qty, unit,
       status (available|locked|consumed), putaway_location, created_at

SupplierInvoice: id, invoice_number, po_id, vendor_id, invoice_amount,
                 invoice_date, received_date,
                 match_status (pending|matched|exception),
                 created_by, created_at

PaymentVoucher: id, voucher_number, invoice_id, amount, payment_method,
                payment_date, journal_entry (JSON), created_by, paid_at
```

#### `production.py`
```
WorkOrder: id, wo_number, fg_material_id, target_qty, unit,
           status (draft|submitted|approved|rejected|in_progress|
                   production_complete|completed),
           approved_by, approved_at, created_by, started_at, completed_at

WOProductionStage: id, wo_id, stage_number (1-6), stage_name,
                   status (pending|done), done_by, done_at

WOLotAllocation: id, wo_id, rm_lot_id, qty_allocated, qty_consumed

FGBatch: id, batch_id, wo_id, material_id, qty, unit,
         status (available|reserved|shipped), produced_at
```

#### `sales.py`
```
SalesOrder: id, so_number, customer_id,
            status (draft|submitted|approved|rejected|picking|
                    shipped|delivered|invoiced|paid|cancelled),
            approved_by, approved_at, created_by, created_at

SOLineItem: id, so_id, material_id, qty_ordered, unit_price,
            batch_id, qty_picked

DeliveryOrder: id, do_number, so_id, driver_name, vehicle_plate,
               shipped_at, delivered_at, status (pending|shipped|delivered),
               created_by

SalesInvoice: id, invoice_number, so_id, customer_id, amount, due_date,
              status (draft|sent|paid|overdue), journal_entry (JSON),
              sent_at, paid_at, created_by

ReceiptVoucher: id, voucher_number, invoice_id, amount, payment_method,
                payment_date, journal_entry (JSON), created_by
```

#### `inventory.py`
```
StockTransaction: id, transaction_type (enum), material_id, lot_id,
                  qty_change (+IN / -OUT), reference_type, reference_id,
                  notes, created_by, created_at

transaction_type enum:
  gr_in | wo_consume | wo_produce | so_ship | adjustment
```

---

### Phase 3 — CSS Design System

From `frontend_style_guide.md`:

| File | Contents |
|------|---------|
| `tokens.css` | All CSS custom properties — colors (4 palettes), typography scale, spacing scale |
| `base.css` | Reset, `body`, `html`, `*` box-sizing, scrollbar |
| `layout.css` | `.layout-wrapper`, `.layout-body`, `.sidebar`, `.navbar`, `.main-content` |
| `components.css` | `.btn`, `.badge`, `.card`, `.table`, `.form-input`, `.form-label` |
| `main.css` | `@import` all 4 files in order |

---

### Phase 4 — Base Templates

| File | Contents |
|------|---------|
| `base.html` | `<!DOCTYPE html>`, Inter font, CSS import, layout blocks, `{% block content %}` |
| `partials/navbar.html` | Top bar — app name, current user, logout link |
| `partials/sidebar.html` | Module nav links — icons + labels, active state by blueprint name |

Sidebar nav items:
```
Dashboard
─────────
Procurement
  └ Purchase Requisitions
  └ Purchase Orders
  └ Goods Receipts
  └ Supplier Invoices
  └ Payments
Production
  └ Work Orders
Sales
  └ Sales Orders
  └ Deliveries
  └ Invoices
  └ Payments Received
Inventory
  └ Stock Ledger
Master Data
  └ Vendors
  └ Customers
  └ Materials
```

---

### Phase 5 — Auth Module

| Route | Method | Template | Access |
|-------|--------|----------|--------|
| `/login` | GET, POST | `auth/login.html` | Public |
| `/logout` | GET | — (redirect) | Logged in |

- Password hashing: `werkzeug.security`
- Session: `flask_login`
- Role decorator: `manager_required`, `warehouse_required`, etc.
- Seed: one default admin user on first run

---

### Phase 6 — Dashboard Module

| Route | Template | Shows |
|-------|----------|-------|
| `/` | `dashboard/index.html` | 4 summary cards + recent activity |

Summary cards:
- RM Stock alerts (lots below ROP)
- Open Purchase Orders count
- Active Work Orders count
- Open Sales Orders count

---

### Phase 7 — Master Data Module

| Route | Action |
|-------|--------|
| `GET /master/vendors` | List all vendors |
| `GET/POST /master/vendors/new` | Create vendor |
| `GET/POST /master/vendors/<id>/edit` | Edit vendor |
| `GET /master/customers` | List all customers |
| `GET/POST /master/customers/new` | Create customer |
| `GET/POST /master/customers/<id>/edit` | Edit customer |
| `GET /master/materials` | List all materials |
| `GET/POST /master/materials/new` | Create material + BOM items |
| `GET/POST /master/materials/<id>/edit` | Edit material |

---

### Phase 8 — Procurement Module (BP-01)

| Route | Action | Status Transition |
|-------|--------|------------------|
| `GET /procurement/pr` | List PRs | — |
| `GET/POST /procurement/pr/new` | Create PR | → Draft |
| `POST /procurement/pr/<id>/submit` | Submit PR | Draft → Submitted |
| `POST /procurement/pr/<id>/approve` | Approve PR | Submitted → Approved |
| `POST /procurement/pr/<id>/reject` | Reject PR | Submitted → Rejected |
| `GET/POST /procurement/po/new/<pr_id>` | Create PO from PR | → Draft |
| `POST /procurement/po/<id>/send` | Send PO | Draft → Sent |
| `POST /procurement/po/<id>/confirm` | Confirm PO | Sent → Confirmed |
| `GET/POST /procurement/gr/new/<po_id>` | Create GR — weight input | → triggers Lot ID |
| `GET/POST /procurement/invoice/new/<po_id>` | Input supplier invoice | — |
| `POST /procurement/invoice/<id>/match` | Run 3-way match | → matched/exception |
| `POST /procurement/invoice/<id>/pay` | Create payment voucher | → Paid |

Business logic to wire in:
- Auto Lot ID: `LOT-YYYYMMDD-NNN`
- Weight variance calc: `(net_weight - po_qty) / po_qty * 100`
- 3-Way Match: compare PO qty/price vs GR net_weight vs Invoice amount within tolerances
- `StockTransaction(type=gr_in)` written on GR save

---

### Phase 9 — Production Module (BP-02)

| Route | Action | Status Transition |
|-------|--------|------------------|
| `GET /production/wo` | List WOs | — |
| `GET/POST /production/wo/new` | Create WO — select material, qty | → Draft |
| `GET /production/wo/<id>` | WO detail — shows FIFO lots, stage checklist | — |
| `POST /production/wo/<id>/submit` | Submit WO | Draft → Submitted |
| `POST /production/wo/<id>/approve` | Approve — lock lots | Submitted → Approved |
| `POST /production/wo/<id>/start` | Start production | Approved → In Progress |
| `POST /production/wo/<id>/stage/<n>` | Mark stage done | updates WOStage |
| `POST /production/wo/<id>/complete` | All 6 stages done | In Progress → Production Complete |
| `POST /production/wo/<id>/finish` | Auto-pass QC, gen Batch ID | Prod Complete → Completed |

Business logic to wire in:
- BOM calculation: `target_qty × bom_qty_per_unit` per RM
- FIFO lot suggestion: `RMLot.query.filter_by(status='available').order_by(created_at)`
- Lot lock on WO approve: `lot.status = 'locked'`
- On WO complete:
  - `lot.status = 'consumed'`
  - `StockTransaction(type=wo_consume, qty_change=-x)` per lot
  - Auto Batch ID: `BATCH-YYYYMMDD-NNN`
  - `StockTransaction(type=wo_produce, qty_change=+x)` for FG

---

### Phase 10 — Sales Module (BP-03)

| Route | Action | Status Transition |
|-------|--------|------------------|
| `GET /sales/so` | List SOs | — |
| `GET/POST /sales/so/new` | Create SO — select customer, add line items | → Draft |
| `GET /sales/so/<id>` | SO detail | — |
| `POST /sales/so/<id>/submit` | Submit SO | Draft → Submitted |
| `POST /sales/so/<id>/approve` | Approve — reserve FG batches FIFO | Submitted → Approved → Picking |
| `POST /sales/so/<id>/pick` | Confirm picking | Picking → Picked |
| `GET/POST /sales/delivery/new/<so_id>` | Create Delivery Order — driver, plate | → Shipped |
| `POST /sales/delivery/<id>/deliver` | Confirm delivery | Shipped → Delivered |
| `POST /sales/so/<id>/invoice` | Generate invoice | Delivered → Invoiced |
| `POST /sales/invoice/<id>/pay` | Create receipt voucher | Invoiced → Paid |

Business logic to wire in:
- FIFO batch reservation: `FGBatch.query.filter_by(status='available').order_by(produced_at)`
- On SO approve: `batch.status = 'reserved'`
- On deliver: `StockTransaction(type=so_ship, qty_change=-x)` + `batch.status = 'shipped'`
- Journal entry on invoice: `{debit: 'AR', credit: 'Revenue', amount: x}`
- Journal entry on payment: `{debit: 'Bank', credit: 'AR', amount: x}`

---

### Phase 11 — Inventory Module

| Route | What it shows |
|-------|--------------|
| `GET /inventory/stock` | Per-material stock balance (SUM of StockTransactions), color-coded vs ROP |
| `GET /inventory/stock/<material_id>` | Transaction ledger for one material |
| `GET /inventory/lots` | All RM lots — ID, material, qty, status, age |
| `GET /inventory/batches` | All FG batches — ID, material, qty, status, produced_at |

Stock balance query (no stored qty):
```python
db.session.query(
    StockTransaction.material_id,
    func.sum(StockTransaction.qty_change).label('balance')
).group_by(StockTransaction.material_id)
```

---

### Phase 12 — Wire-up & Verify

```bash
pip install -r requirements.txt
flask db init
flask db migrate -m "initial schema"
flask db upgrade
flask shell  # seed admin user
flask run
```

**Smoke test checklist:**
- [ ] `http://localhost:5000/login` loads
- [ ] Login with seeded admin works
- [ ] Sidebar shows all 7 modules
- [ ] All list pages load without 500 error
- [ ] `wfims.db` file created at project root

---

## Auto-generated Document Numbers

| Document | Format | Example |
|----------|--------|---------|
| Purchase Requisition | `PR-YYYYMMDD-NNN` | `PR-20260511-001` |
| Purchase Order | `PO-YYYYMMDD-NNN` | `PO-20260511-001` |
| Goods Receipt | `GR-YYYYMMDD-NNN` | `GR-20260511-001` |
| RM Lot | `LOT-YYYYMMDD-NNN` | `LOT-20260511-001` |
| Payment Voucher | `PV-YYYYMMDD-NNN` | `PV-20260511-001` |
| Work Order | `WO-YYYYMMDD-NNN` | `WO-20260511-001` |
| FG Batch | `BATCH-YYYYMMDD-NNN` | `BATCH-20260511-001` |
| Sales Order | `SO-YYYYMMDD-NNN` | `SO-20260511-001` |
| Delivery Order | `DO-YYYYMMDD-NNN` | `DO-20260511-001` |
| Sales Invoice | `INV-YYYYMMDD-NNN` | `INV-20260511-001` |
| Receipt Voucher | `RV-YYYYMMDD-NNN` | `RV-20260511-001` |

---

## Dependencies (`requirements.txt`)

```
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-Migrate==4.0.7
Werkzeug==3.1.3
python-dotenv==1.0.1
```

---

## Progress Tracker

See `.context/development/progress.md` — updated after each phase completes.
