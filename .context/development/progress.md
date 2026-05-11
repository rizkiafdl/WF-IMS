# WF-IMS MVP — Build Progress

> Updated after each phase completes.
> Reference: `implementation_plan.md`

---

## Phase Status

| Phase | Description | Status | Completed |
|-------|-------------|:------:|-----------|
| 1 | Foundation — config, run, app factory, extensions | ✅ | 2026-05-11 |
| 2 | Database Models — all 6 model files | ✅ | 2026-05-11 |
| 3 | CSS Design System — tokens, base, layout, components | ✅ | 2026-05-11 |
| 4 | Base Templates — base.html, navbar, sidebar | ✅ | 2026-05-11 |
| 5 | Auth Module — login, logout, role guard | ✅ | 2026-05-11 |
| 6 | Dashboard Module — home, summary cards | ✅ | 2026-05-11 |
| 7 | Master Data — vendor, customer, material CRUD | ✅ | 2026-05-11 |
| 8 | Procurement Module — PR → PO → GR → Invoice → Pay | ✅ | 2026-05-11 |
| 9 | Production Module — WO → stages → FG batch | ⬜ | — |
| 10 | Sales Module — SO → pick → deliver → invoice → pay | ⬜ | — |
| 11 | Inventory Module — stock ledger, lot view | ⬜ | — |
| 12 | Wire-up & Verify — flask run, db upgrade, smoke test | ⬜ | — |

---

## Issues / Decisions Log

> Record any blockers, deviations from plan, or decisions made during build.

| # | Phase | Issue | Decision | Date |
|---|-------|-------|----------|------|
| 1 | 5–8 | Phases 9–11 sidebar links would 500 before registration | Added stub blueprints for production/sales/inventory (coming_soon.html) | 2026-05-11 |
| 2 | 5 | seed-admin CLI command added | `flask seed-admin` creates admin@wfims.com / admin123 | 2026-05-11 |

---

## Known Deferred Items

> Things intentionally skipped during build — carry forward to Phase 2.

| Item | Original location | Phase 2 plug-in point |
|------|------------------|-----------------------|
| QC inspection (8 ENplus params) | BP-02 Production | After Production Complete state |
| Rework / Scrap flow | BP-02 Production | Replaces auto-pass QC |
| Return-to-Supplier | BP-01 Procurement | After GR weight rejection |
| Credit limit check | BP-03 Sales | Before SO approval |
| Supplier Scorecard | BP-01 Procurement | After payment / return |
| CoA generation | BP-02 → BP-03 | After QC pass |
| HPP cost tracking | BP-02 per stage | Inside WOProductionStage |
| Auto payment reminders | BP-03 Finance | After invoice due_date passes |