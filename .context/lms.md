# 🔄 WF-IMS — Business Process Documentation

> **Project:** Wood Fuel Integrated Management System  
> **Version:** 1.0

---

## 1. Proses Bisnis Utama (End-to-End)

```mermaid
graph LR
    A[📦 Procurement] --> B[🏭 Warehouse IN]
    B --> C[⚙️ Production]
    C --> D[✅ Quality Control]
    D --> E[📦 Warehouse OUT]
    E --> F[🚚 Sales & Distribution]
    F --> G[💰 Finance]
    
    style A fill:#e3f2fd
    style B fill:#e8f5e9
    style C fill:#fff3e0
    style D fill:#fce4ec
    style E fill:#e8f5e9
    style F fill:#f3e5f5
    style G fill:#fff9c4
```

---

## 2. BP-01: Procure-to-Pay (P2P) — Pengadaan Bahan Baku

### Overview
| Aspek | Detail |
|-------|--------|
| **Trigger** | Stok bahan baku di bawah minimum / permintaan produksi |
| **End State** | Pembayaran ke supplier selesai, stok bahan baku bertambah |
| **Aktor** | Admin, Manager, Supplier, Staff Gudang, Tim Keuangan |
| **Durasi Tipikal** | 3-7 hari kerja |

### Alur Proses

```mermaid
graph TD
    A["Alert - Stok di bawah minimum"] --> B["Admin buat Purchase Requisition"]
    B --> C{"Manager approve PR?"}
    C -->|Ya| D["Admin buat Purchase Order"]
    C -->|Tidak| Z1["PR ditolak atau revisi"]
    D --> E["PO dikirim ke Supplier via Portal"]
    E --> F{"Supplier konfirmasi PO?"}
    F -->|Accept| G["Supplier kirim barang"]
    F -->|Negosiasi| H["Admin review perubahan"]
    F -->|Reject| Z2["Cari supplier lain"]
    H --> D
    G --> I["Staff Gudang - Goods Receipt"]
    I --> J["Input timbangan bruto-tara=netto"]
    J --> K{"Berat sesuai PO? Toleransi 5%"}
    K -->|Ya| L["Terima dan generate Lot ID"]
    K -->|Selisih besar| M{"Terima partial?"}
    M -->|Ya| L
    M -->|Tidak| Z3["Tolak penerimaan"]
    L --> N["Catat kadar air per lot"]
    N --> O["Putaway ke lokasi penyimpanan"]
    O --> P["Stok bahan baku bertambah"]
    P --> Q["Three-Way Matching PO vs GR vs Invoice"]
    Q --> R{"Cocok?"}
    R -->|Ya| S["Tim Keuangan - Buat Payment Voucher"]
    R -->|Tidak| T["Flag exception review manual"]
    S --> U["Proses pembayaran ke supplier"]
    U --> V["Jurnal - Debit Hutang Kredit Bank"]
```

### Business Rules
1. **PR → PO**: Setiap pembelian harus melalui PR yang diapprove Manager
2. **Toleransi Berat**: Selisih timbangan ±5% dari qty PO, lebih dari itu butuh approval
3. **Lot Classification**: Moisture < 15% (siap produksi), 15-30% (perlu drying), > 30% (terlalu basah)
4. **Three-Way Matching**: PO, GR, dan Invoice supplier harus cocok sebelum pembayaran

---

## 3. BP-02: Produce-to-Stock — Proses Produksi

### Overview
| Aspek | Detail |
|-------|--------|
| **Trigger** | Kebutuhan produksi / stok produk jadi rendah |
| **End State** | Batch pellet yang QC passed masuk stok produk jadi |
| **Aktor** | Staff Produksi, Staff QC, Manager |
| **Durasi Tipikal** | 1-3 hari per batch |

### Alur Proses

```mermaid
graph TD
    A["Staff Produksi - Buat Work Order"] --> B["Pilih BOM dan target output"]
    B --> C["Sistem hitung kebutuhan bahan baku"]
    C --> D{"Stok BB cukup?"}
    D -->|Ya| E["Alokasi lot bahan baku - prioritas FIFO"]
    D -->|Tidak| Z1["Tunda WO atau buat PR"]
    E --> F{"Manager approve WO?"}
    F -->|Ya| G["Status Approved, lot di-lock"]
    F -->|Tidak| Z2["WO rejected"]
    
    G --> H["Tahap 1 CHIPPING - potong kayu jadi chip"]
    H --> I["Tahap 2 DRYING - keringkan chip, catat BBM"]
    I --> J["Tahap 3 PELLETING - cetak pellet 6-8mm"]
    J --> K["Tahap 4 COOLING - dinginkan ke suhu ruang"]
    K --> L["Tahap 5 SCREENING - saring, pisahkan fines"]
    L --> M["Tahap 6 PACKING - karung 25kg, label"]
    
    M --> N["Production Complete"]
    N --> O["QC - Uji 8 parameter ENplus"]
    O --> P{"Semua parameter PASS?"}
    P -->|Ya| Q["Grade A1 atau A2 atau B"]
    P -->|Tidak| R{"Bisa rework?"}
    R -->|Ya| S["Rework - kembali ke tahap relevan"]
    S --> O
    R -->|Tidak| T{"Bisa downgrade?"}
    T -->|Ya| U["Downgrade grade"]
    T -->|Tidak| V["SCRAP - catat sebagai rugi"]
    
    Q --> W["Generate CoA"]
    W --> X["Stok produk jadi bertambah"]
    X --> Y["Batch available untuk Sales Order"]
```

### 6 Tahap Produksi — Detail Input/Output

| Tahap | Proses | Input | Output | Waste | Durasi Est. |
|:-----:|--------|-------|--------|-------|:-----------:|
| 1 | **Chipping** | Kayu gelondongan | Wood chip kecil | Kulit, potongan (~1%) | 4 jam |
| 2 | **Drying** | Chip basah (~18%) | Chip kering (<12%) | Uap air (~15%) | 17 jam |
| 3 | **Pelleting** | Chip kering | Pellet 6-8mm | Debu, fines (~2%) | 8 jam |
| 4 | **Cooling** | Pellet panas | Pellet suhu ruang | Minimal | 2 jam |
| 5 | **Screening** | Pellet mixed | Pellet grade OK | Fines (<3.15mm) | 1.5 jam |
| 6 | **Packing** | Pellet OK | Karung 25kg berlabel | — | 2 jam |

### Business Rules
1. **FIFO Lot**: Lot yang masuk lebih dulu diprioritaskan untuk produksi
2. **Lot Lock**: Lot yang dialokasikan ke WO tidak bisa dipakai WO lain
3. **QC Wajib**: Stok HANYA bertambah setelah QC PASSED
4. **Rework**: Moisture fail → re-dry, fines fail → re-screen, durability fail → re-pellet
5. **HPP Tracking**: Setiap tahap mencatat biaya untuk kalkulasi HPP per batch

---

## 4. BP-03: Order-to-Cash (O2C) — Penjualan & Penagihan

### Overview
| Aspek | Detail |
|-------|--------|
| **Trigger** | Pesanan pelanggan masuk (telepon/portal) |
| **End State** | Pembayaran pelanggan diterima, piutang lunas |
| **Aktor** | Admin/Pelanggan, Manager, Staff Gudang, Tim Keuangan |
| **Durasi Tipikal** | 2-5 hari (kirim) + 30-60 hari (bayar) |

### Alur Proses

```mermaid
graph TD
    A["Pelanggan pesan via telepon, email, portal"] --> B["Admin buat Sales Order"]
    B --> C{"Credit limit cukup?"}
    C -->|Ya| D{"Stok pellet cukup?"}
    C -->|Tidak| Z1["Tolak atau minta bayar dulu"]
    D -->|Ya| E{"Manager approve SO?"}
    D -->|Tidak| Z2["Partial delivery atau backorder"]
    E -->|Ya| F["SO Approved, stok reserved"]
    E -->|Tidak| Z3["SO rejected"]
    
    F --> G["Staff Gudang - Picking batch FIFO"]
    G --> H["Packing ke karung 25kg"]
    H --> I["Timbang berat keluar"]
    I --> J["Generate Surat Jalan + lampirkan CoA"]
    J --> K["Loading ke truk"]
    
    K --> L["Input data driver dan kendaraan"]
    L --> M["Truk berangkat - status Shipped"]
    M --> N["Monitor perjalanan"]
    N --> O{"Pelanggan terima barang?"}
    O -->|Ya OK| P["Konfirmasi delivery"]
    O -->|Komplain| Z4["Proses return retur"]
    
    P --> Q["Admin - Generate Invoice"]
    Q --> R["Jurnal Debit Piutang Kredit Penjualan"]
    R --> S["Kirim invoice ke pelanggan"]
    S --> T["Monitor jatuh tempo"]
    
    T --> U{"Pembayaran masuk?"}
    U -->|Ya| V["Buat Receipt Voucher"]
    U -->|Overdue| W["Kirim reminder"]
    W --> U
    V --> X["Jurnal Debit Bank Kredit Piutang"]
    X --> Y["Invoice LUNAS"]
```

### Business Rules
1. **Credit Check**: SO tidak bisa dibuat jika melebihi credit limit (kecuali Manager override)
2. **Stok Check**: Hanya batch QC PASSED yang bisa dijual
3. **FIFO Picking**: Batch produksi paling lama diprioritaskan untuk pengiriman
4. **Auto-Journal**: Invoice otomatis membuat jurnal piutang
5. **Payment Terms**: Sesuai setting per pelanggan (COD / Net 30 / Net 60)

---

## 5. BP-04: Quality Assurance — Kontrol Kualitas

### Overview
| Aspek | Detail |
|-------|--------|
| **Trigger** | Batch produksi selesai (Production Complete) |
| **End State** | Batch mendapat grade & CoA, atau di-rework/scrap |
| **Aktor** | Staff QC, Manager |
| **Standar Acuan** | ENplus (ISO 17225-2) |

### Alur Proses

```mermaid
graph TD
    A["Batch production complete"] --> B["Staff QC ambil sampel 5 titik"]
    
    B --> C1["Uji 1 Moisture Content EN 14774"]
    B --> C2["Uji 2 Ash Content EN 14775"]
    B --> C3["Uji 3 Calorific Value EN 14918"]
    B --> C4["Uji 4 Diameter EN 16127"]
    B --> C5["Uji 5 Length"]
    B --> C6["Uji 6 Durability EN 15210"]
    B --> C7["Uji 7 Fines Content EN 15149"]
    B --> C8["Uji 8 Bulk Density EN 15103"]
    
    C1 --> D["Input semua hasil ke sistem"]
    C2 --> D
    C3 --> D
    C4 --> D
    C5 --> D
    C6 --> D
    C7 --> D
    C8 --> D
    
    D --> E{"Semua 8 parameter PASS?"}
    E -->|Ya| F["Tentukan grade berdasarkan parameter terketat"]
    E -->|Tidak| G["Identifikasi parameter yang fail"]
    
    F --> H["Status PASSED - Grade A1 A2 B"]
    H --> I["Generate CoA - tanda tangan inspector + manager"]
    I --> J["Batch masuk stok produk jadi"]
    
    G --> K{"Fail type?"}
    K -->|Moisture tinggi| L["Rework Re-Drying"]
    K -->|Fines tinggi| M["Rework Re-Screening"]
    K -->|Durability rendah| N["Rework Re-Pelleting"]
    K -->|Ash Kalor| O{"Bisa downgrade?"}
    O -->|Ya| P["Downgrade A1 ke A2 atau A2 ke B"]
    O -->|Tidak| Q["SCRAP - catat sebagai rugi produksi"]
    
    L --> R["QC ulang setelah rework"]
    M --> R
    N --> R
    R --> E
```

### Standar Kualitas ENplus

| Parameter | A1 | A2 | B | Metode |
|-----------|:---:|:---:|:---:|--------|
| Moisture | ≤ 10% | ≤ 10% | ≤ 10% | EN 14774-1 |
| Ash | ≤ 0.7% | ≤ 1.2% | ≤ 3.0% | EN 14775 |
| Calorific Value | ≥ 16.5 MJ/kg | ≥ 16.5 MJ/kg | ≥ 16.5 MJ/kg | EN 14918 |
| Diameter | 6±1 / 8±1 mm | Sama | Sama | EN 16127 |
| Length | 3.15-40 mm | Sama | Sama | — |
| Durability | ≥ 98.0% | ≥ 98.0% | ≥ 97.5% | EN 15210-1 |
| Fines | ≤ 0.5% | ≤ 0.5% | ≤ 1.0% | EN 15149-1 |
| Bulk Density | ≥ 600 kg/m³ | Sama | Sama | EN 15103 |

---

## 6. BP-05: Financial Close — Penutupan Keuangan

### Alur Proses

```mermaid
graph TD
    A["Akhir periode - bulanan"] --> B["Verifikasi semua voucher sudah posted"]
    B --> C["Rekonsiliasi bank - saldo sistem vs mutasi bank"]
    C --> D["Stock opname - stok fisik vs stok sistem"]
    D --> E{"Ada selisih?"}
    E -->|Ya| F["Buat jurnal adjustment"]
    E -->|Tidak| G["Lanjut"]
    F --> G
    G --> H["Hitung penyusutan aset bulan ini"]
    H --> I["Buat jurnal penyusutan"]
    I --> J["Review semua piutang - ada bad debt?"]
    J --> K["Review semua hutang - ada yang jatuh tempo?"]
    K --> L["Generate Laporan Laba Rugi"]
    L --> M["Generate Neraca"]
    M --> N{"Neraca balance? Aset = L + E"}
    N -->|Ya| O["Generate Arus Kas"]
    N -->|Tidak| P["Review jurnal - cari kesalahan"]
    P --> B
    O --> Q["Owner review dan approve laporan"]
    Q --> R["Arsip laporan keuangan periode ini"]
```

---

## 7. BP-06: Inventory Management — Siklus Stok

```mermaid
graph TD
    subgraph "INBOUND - Stok Masuk"
        A1["GR dari supplier"] -->|stok BB naik| S["STOK"]
        A2["QC Passed"] -->|stok PJ naik| S
    end
    
    subgraph "OUTBOUND - Stok Keluar"
        S -->|stok BB turun| B1["Alokasi ke Work Order"]
        S -->|stok PJ turun| B2["Picking untuk Sales Order"]
    end
    
    subgraph "ADJUSTMENT"
        S -->|adjust| C1["Stock Opname"]
        S -->|adjust| C2["Rework atau Scrap"]
        S -->|adjust| C3["Susut alami"]
    end
    
    subgraph "MONITORING"
        S --> D1{"Stok di bawah minimum?"}
        D1 -->|Ya| D2["Alert - buat PR"]
        S --> D3["Dashboard real-time"]
        S --> D4["Lot traceability"]
    end
```

### Tipe Mutasi Stok

| Tipe | Simbol | Trigger | Contoh |
|------|:------:|---------|--------|
| **IN** | 🟢 | GR, QC Pass | Penerimaan BB, batch QC passed |
| **OUT** | 🔴 | WO consume, SO ship | Produksi pakai lot, pengiriman pelanggan |
| **ADJ+** | 🟡 | Opname surplus | Stock opname: fisik > sistem |
| **ADJ-** | 🟡 | Opname kurang, scrap | Stock opname: fisik < sistem, batch scrap |

---

## 8. BP-07: Portal Supplier Workflow

```mermaid
sequenceDiagram
    participant Admin as Admin WF-IMS
    participant Sistem as Sistem
    participant Supplier as Portal Supplier
    
    Admin->>Sistem: Buat PO
    Sistem->>Supplier: Notifikasi PO baru
    
    Supplier->>Sistem: Review PO
    
    alt Accept
        Supplier->>Sistem: Konfirmasi PO + estimasi kirim
        Sistem->>Admin: Notifikasi PO dikonfirmasi
    else Negosiasi
        Supplier->>Sistem: Request perubahan harga dan jadwal
        Sistem->>Admin: Notifikasi perlu review
        Admin->>Sistem: Update PO
        Sistem->>Supplier: PO updated
    else Reject
        Supplier->>Sistem: Tolak PO + alasan
        Sistem->>Admin: Notifikasi PO ditolak
    end
    
    Note over Supplier: Saat barang siap kirim
    
    Supplier->>Sistem: Update pengiriman driver nopol foto
    Sistem->>Admin: Notifikasi barang dikirim
    Sistem->>Admin: Notifikasi siapkan area penerimaan
    
    Note over Supplier: Setelah pembayaran
    
    Supplier->>Sistem: Cek status pembayaran
    Sistem->>Supplier: Tampilkan riwayat dan status bayar
```

---

## 9. BP-08: Portal Pelanggan Workflow

```mermaid
sequenceDiagram
    participant Cust as Portal Pelanggan
    participant Sistem as Sistem
    participant Admin as Admin WF-IMS
    participant Gudang as Staff Gudang
    
    Cust->>Sistem: Buat order self-service
    Sistem->>Sistem: Cek credit limit
    Sistem->>Admin: Notifikasi order baru dari portal
    
    Admin->>Sistem: Review dan approve SO
    Sistem->>Cust: Notifikasi order dikonfirmasi
    
    Gudang->>Sistem: Picking dan packing
    Gudang->>Sistem: Kirim dan update status
    Sistem->>Cust: Notifikasi pesanan dikirim
    
    Cust->>Sistem: Tracking pengiriman
    Sistem->>Cust: Status real-time
    
    Note over Cust: Barang tiba
    
    Cust->>Sistem: Download dokumen
    Note right of Cust: Invoice Surat Jalan CoA
```

---

## 10. Cross-Module Integration Map

```mermaid
graph TB
    subgraph "MODULE DEPENDENCIES"
        INV["Inventori"]
        WH["Gudang"]
        PROD["Produksi"]
        QC["Quality Control"]
        SALE["Penjualan"]
        SUP["Supplier"]
        FIN["Keuangan"]
        ANA["Analytics"]
    end
    
    SUP -->|PO| WH
    WH -->|GR Lot| INV
    INV -->|Lot allocation| PROD
    PROD -->|Batch| QC
    QC -->|Passed batch| INV
    INV -->|Stock available| SALE
    SALE -->|Picking request| WH
    WH -->|Shipment| SALE
    
    SUP -->|Invoice match| FIN
    SALE -->|Invoice| FIN
    PROD -->|HPP data| FIN
    
    INV -->|Stock data| ANA
    PROD -->|Output efficiency| ANA
    QC -->|Quality trends| ANA
    SALE -->|Revenue| ANA
    FIN -->|Profit margin| ANA
```

---

## 11. Status & State Machines

### Sales Order States

```mermaid
stateDiagram-v2
    [*] --> Draft: Buat SO
    Draft --> PendingApproval: Submit
    PendingApproval --> Approved: Manager OK
    PendingApproval --> Rejected: Manager tolak
    Rejected --> [*]
    Approved --> Picking: Assign ke gudang
    Picking --> ReadyToShip: Pack selesai
    ReadyToShip --> Shipped: Truk berangkat
    Shipped --> Delivered: Pelanggan terima
    Delivered --> Invoiced: Invoice dibuat
    Invoiced --> Paid: Pembayaran lunas
    Paid --> [*]
    
    Approved --> Cancelled: Admin batal
    Cancelled --> [*]
```

### Work Order States

```mermaid
stateDiagram-v2
    [*] --> Draft: Buat WO
    Draft --> Approved: Manager OK
    Draft --> Rejected: Manager tolak
    Rejected --> [*]
    Approved --> InProgress: Mulai produksi
    InProgress --> ProductionComplete: 6 tahap selesai
    ProductionComplete --> QCPending: Submit ke QC
    QCPending --> QCPassed: Semua parameter pass
    QCPending --> QCFailed: Ada parameter fail
    QCFailed --> Rework: Bisa diperbaiki
    QCFailed --> Scrapped: Tidak bisa diperbaiki
    Rework --> QCPending: QC ulang
    Scrapped --> [*]
    QCPassed --> Completed: Masuk stok
    Completed --> [*]
```

### Purchase Order States

```mermaid
stateDiagram-v2
    [*] --> Draft: Buat PO
    Draft --> Sent: Kirim ke supplier
    Sent --> Confirmed: Supplier terima
    Sent --> Rejected: Supplier tolak
    Rejected --> [*]
    Confirmed --> InTransit: Supplier kirim barang
    InTransit --> Received: GR full
    InTransit --> PartiallyReceived: GR partial
    PartiallyReceived --> Received: Sisa diterima
    Received --> Completed: Pembayaran lunas
    Completed --> [*]
```