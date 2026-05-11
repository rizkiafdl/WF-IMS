# User Roles & Permissions — MVP

> For MVP, roles are kept minimal. One user can hold multiple roles.

---

## Roles

| Role | Description |
|------|-------------|
| **Admin** | General operations — creates PRs, POs, SOs, invoices |
| **Manager** | Approves PRs, WOs, SOs. Has override rights |
| **Warehouse Staff** | Handles GR, putaway, picking, shipment confirmation |
| **Production Staff** | Creates and progresses Work Orders |
| **Finance** | Handles invoices, payment vouchers, 3-way match |

> For a small demo, Admin + Manager can be a single "superuser" role.

---

## Permission Matrix

### BP-01 — Procurement

| Action | Admin | Manager | Warehouse | Production | Finance |
|--------|:-----:|:-------:|:---------:|:----------:|:-------:|
| Create PR | ✅ | ✅ | — | — | — |
| Approve / Reject PR | — | ✅ | — | — | — |
| Create PO | ✅ | — | — | — | — |
| Mark PO as Sent | ✅ | — | — | — | — |
| Confirm PO (supplier action) | ✅ | — | — | — | — |
| Create Goods Receipt | — | — | ✅ | — | — |
| Generate Lot ID | — | — | ✅ | — | — |
| Input Supplier Invoice | ✅ | — | — | — | ✅ |
| Run 3-Way Match | — | — | — | — | ✅ |
| Create Payment Voucher | — | — | — | — | ✅ |
| Mark Payment as Paid | — | — | — | — | ✅ |

### BP-02 — Production

| Action | Admin | Manager | Warehouse | Production | Finance |
|--------|:-----:|:-------:|:---------:|:----------:|:-------:|
| Create Work Order | — | — | — | ✅ | — |
| Approve / Reject WO | — | ✅ | — | — | — |
| Progress production stages | — | — | — | ✅ | — |
| Mark Production Complete | — | — | — | ✅ | — |
| Confirm FG to inventory | — | — | ✅ | ✅ | — |

### BP-03 — Sales

| Action | Admin | Manager | Warehouse | Production | Finance |
|--------|:-----:|:-------:|:---------:|:----------:|:-------:|
| Create Sales Order | ✅ | — | — | — | — |
| Approve / Reject SO | — | ✅ | — | — | — |
| Pick & pack batches | — | — | ✅ | — | — |
| Generate Delivery Order | — | — | ✅ | — | — |
| Mark as Shipped | — | — | ✅ | — | — |
| Confirm Delivery | ✅ | — | — | — | — |
| Generate Invoice | ✅ | — | — | — | ✅ |
| Create Receipt Voucher | — | — | — | — | ✅ |
| Mark Invoice as Paid | — | — | — | — | ✅ |

---

## Flask Implementation Note

Use a simple `role` field on the `users` table (enum or string). No complex RBAC library needed for MVP — just check `current_user.role` in route decorators or Jinja2 templates.

```python
# Example role check in Flask
def manager_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role not in ['manager', 'admin']:
            abort(403)
        return f(*args, **kwargs)
    return decorated
```
