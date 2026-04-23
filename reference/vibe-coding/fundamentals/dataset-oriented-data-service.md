# Dataset-Oriented Data Service Protocol

## 适用场景
- 构建数据采集服务时
- 设计 Data Pipeline 时
- 规范化数据仓库结构时

## 触发条件
- 创建新的数据采集服务
- 接入外部数据源
- 定义数据交付边界

---

## IF-THEN Rules

### 1. Core Design Philosophy

**IF** designing a data service  
**THEN** apply: **Dataset First, Schema/Contract First, Shared Control Plane**

**IF** determining if this template applies  
**THEN** use this decision rule:
> **IF** core deliverable is "stable dataset" (not "page" or "API"), **THEN** use this template

---

### 2. Directory Structure Template

**IF** creating a dataset-oriented service  
**THEN** use this standard structure:

```
<service-root>/
├── README.md
├── AGENTS.md
├── pyproject.toml
├── scripts/
│   ├── start.sh
│   ├── verify.sh
│   └── check_legacy_shells.sh
├── src/<service_name>/
│   ├── config.py
│   ├── registry.py
│   ├── service_entry.py
│   ├── common/ (env, io, time, symbols, shared utils)
│   ├── runtime/ (stack_runner, process_utils, group_runners)
│   ├── writers/
│   ├── validators/
│   └── datasets/
│       ├── <dataset_a>/ (contract, collect, backfill, repair, writer, validate)
│       ├── <dataset_b>/
│       └── _reserved/
├── tests/
└── legacy/ (migration period)
```

---

### 3. Dataset Implementation Unit

**IF** implementing a dataset  
**THEN** create these standard files:

| File | Purpose |
|------|---------|
| `contract.py` | Define dataset key, resource_id, physical table, primary/idempotent keys, time semantics, field semantics |
| `collect.py` | Real-time or polling collection logic |
| `backfill.py` | Historical data backfill, file import, pagination |
| `repair.py` | Gap repair, exception recovery, partial recalculation |
| `writer.py` | Unified storage, batch write, deduplication, conflict handling |
| `validate.py` | Data quality checks, row count, field, time continuity |

**IF** a dataset lacks certain capabilities (repair/backfill)  
**THEN** explicitly mark as unsupported in registry, don't silently omit

---

### 4. Registry (Single Source of Truth)

**IF** creating registry  
**THEN** define these minimum fields:

```python
dataset_key: str
resource_id: str
runtime_status: active | backfill_only | reserved | disabled
physical_table: str
group: lf | hf | events | snapshots
source_kind: ws | rest | zip | scrape | file | api
collect_supported: bool
backfill_supported: bool
repair_supported: bool
default_enabled: bool
owner: str
```

---

### 5. Dataset Naming Rules

**IF** naming datasets  
**THEN** use this pattern:

```
<market>_<instrument>_<topic>_<granularity?>_<layer?>
```

**EXAMPLES:**
- `spot_trades`
- `futures_um_trades`
- `futures_um_book_ticker`
- `futures_um_book_depth`
- `candles_1m`
- `futures_metrics_5m`
- `futures_um_metrics_atomic`

**IF** naming  
**THEN** express WHAT the data is, not HOW it's implemented

---

### 6. Data Model Layers

**IF** designing data models  
**THEN** distinguish between these layers:

| Layer | Description |
|-------|-------------|
| atomic | Atomic events/raw records |
| snapshot | Single polling snapshots |
| bucketed | Time-window aggregated results |
| derived | Derived from fact layer |
| reserved | Reserved but not enabled |

---

### 7. Service Entry Protocol

**IF** implementing service entry  
**THEN** provide these actions only:
- `plan` - Show execution plan
- `start` - Start service
- `stop` - Stop service
- `status` - Show current status
- `restart` - Restart service

**IF** implementing runtime  
**THEN** handle:
- Process orchestration
- Mode grouping (lf/hf/events/snapshots)
- PID/log/health management
- cold-start/restart/stop behavior

**IF** writing business logic  
**THEN** do NOT implement your own daemon/control plane

---

### 8. New Service Creation Workflow

**IF** creating a new data service from scratch  
**THEN** follow this sequence:

```
Step 1: Define Dataset List
  └─ Identify deliverables, physical tables
  └─ Mark active/backfill_only/reserved status

Step 2: Write Contracts First
  └─ Fields, keys, time columns, partition strategy
  └─ Resource ID, schema version

Step 3: Build Shared Control Plane
  └─ config.py, registry.py, service_entry.py, runtime/

Step 4: Implement Datasets
  └─ contract → writer → collect → backfill → validate → repair

Step 5: Complete Documentation & Gates
  └─ README, AGENTS, verify/CI, lineage mapping, smoke tests
```

---

### 9. External Source Integration Workflow

**IF** integrating external source code  
**THEN** follow this refactoring process:

```
Step 1: Inventory, Don't Copy
  └─ Identify actual data objects and tables
  └─ Classify: collect / backfill / repair / utility

Step 2: Reverse-Map to Datasets
  └─ Multiple scripts → abstract to datasets
  └─ Create contract/writer/collect/backfill per dataset

Step 3: Extract Common Capabilities
  └─ Move to common/runtime/writers:
  └─ API client, auth, rate limiter, symbol normalize, storage, retry, downloader

Step 4: Explicit Legacy Isolation
  └─ Keep old entry points as compatibility wrappers only
  └─ No new logic in legacy paths
  └─ Add gate to prevent backflow
```

---

## Key Concept Index

| Concept | Definition |
|---------|------------|
| Dataset | Boundary for development, scheduling, deployment, ops, lineage, permissions |
| Contract | Schema/data contract as stable source of truth |
| Registry | Single source of truth for dataset inventory |
| Service Entry | Unified internal entry point (plan/start/stop/status/restart) |
| Runtime | Unified execution plane (process orchestration) |
| Backfill | Historical data backfill operations |
| Repair | Gap repair and exception recovery |
| Writer | Unified storage and batch write layer |
| Validator | Data quality verification layer |
