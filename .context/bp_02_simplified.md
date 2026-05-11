# BP-02: Production (Simplified) — Produce-to-Stock

> QC auto-passed for MVP. Rework, scrap, and HPP tracking deferred to Phase 2.

---

## Glossary

| Term | Meaning |
|------|---------|
| **WO** | Work Order — the job ticket to run a production batch |
| **BOM** | Bill of Materials — how much raw material is needed per unit of output |
| **Lot (RM)** | Raw material lot from GR, tracked by Lot ID |
| **Batch (FG)** | Finished goods output from one WO, gets its own Batch ID |
| **FIFO** | First In First Out — oldest RM lots consumed first |
| **Lot Lock** | RM lots allocated to a WO cannot be used by another WO |
| **FG** | Finished Goods — wood pellets ready for sale |

---

## BP-02: Produce-to-Stock (MVP Simplified)

### Overview

| Aspect | Detail |
|--------|--------|
| Trigger | Low finished goods stock OR manual creation by Production Staff |
| End State | FG batch available in inventory, ready for Sales Order |
| Actors | Production Staff, Manager, Warehouse Staff |
| Typical Duration | 1–2 days per batch |
| Scope (MVP) | Work Order → material consumption → production stages → FG stock IN |
| Out of Scope | QC inspection, rework, scrap, HPP cost tracking, CoA generation |

### Process Flow

```mermaid
graph TD
    A["Trigger: Low FG stock OR manual request"] --> B["Production Staff creates Work Order"]
    B --> C["Select material output + target qty"]
    C --> D["System calculates RM needed via BOM"]
    D --> E{"RM stock sufficient?"}
    E -->|No| Z1["Block WO — alert to create PR"]
    E -->|Yes| F["System suggests RM lots (FIFO order)"]
    F --> G["Production Staff confirms lot allocation"]
    G --> H{"Manager approves WO?"}
    H -->|No| Z2["WO rejected"]
    H -->|Yes| I["WO Approved — lots locked"]
    I --> J["Stage 1: Chipping ✓"]
    J --> K["Stage 2: Drying ✓"]
    K --> L["Stage 3: Pelleting ✓"]
    L --> M["Stage 4: Cooling ✓"]
    M --> N["Stage 5: Screening ✓"]
    N --> O["Stage 6: Packing ✓"]
    O --> P["Mark Production Complete"]
    P --> Q["Auto-pass QC (MVP)"]
    Q --> R["Generate Batch ID for FG"]
    R --> S["RM lot stock decremented"]
    S --> T["FG batch added to inventory (status: Available)"]
    T --> U["WO Completed"]
```

### Production Stages (MVP)

Each stage is a simple checkbox/status toggle — no detailed input required for MVP.

| Stage | Name | What staff marks |
|:-----:|------|-----------------|
| 1 | Chipping | Done / timestamp |
| 2 | Drying | Done / timestamp |
| 3 | Pelleting | Done / timestamp |
| 4 | Cooling | Done / timestamp |
| 5 | Screening | Done / timestamp |
| 6 | Packing | Done / timestamp |

### Business Rules (MVP)

| Rule ID | Description | Value |
|---------|-------------|-------|
| BR-02.1 | WO requires Manager approval before production starts | Enforced |
| BR-02.2 | RM lots allocated to a WO are locked — no other WO can use them | Enforced |
| BR-02.3 | FIFO lot selection — oldest GR date first | Enforced |
| BR-02.4 | RM stock decremented only when WO reaches Completed | On completion |
| BR-02.5 | FG stock added only when WO reaches Completed | On completion |
| BR-02.6 | QC auto-passed for MVP — all completed batches go directly to Available | MVP rule |

### State Machine

**WO States:**
`Draft → Submitted → Approved | Rejected → In Progress → Production Complete → Completed`

### What's Deferred to Phase 2

| Deferred | Plug-in point |
|----------|---------------|
| QC inspection (8 ENplus parameters) | Between Production Complete and Completed |
| Rework flow | Replaces auto-pass when QC fails |
| Scrap flow | Replaces auto-pass when rework not possible |
| CoA generation | After QC Passed |
| HPP cost tracking per stage | Inside each stage step |
| Waste/yield recording per stage | Inside each stage step |
