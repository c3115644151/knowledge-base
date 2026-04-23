# Project Architecture Template Protocol

## 适用场景
- 初始化新 Python/Web/Data Science 项目时
- 设计 Monorepo 或 Full-Stack 应用时
- 制定团队代码组织规范时

## 触发条件
- 创建新项目
- 重构现有项目结构
- 团队需要统一项目模板

---

## IF-THEN Rules

### 1. Python Web/API Project Structure

**IF** building a Flask/FastAPI Web application or RESTful API  
**THEN** use this directory structure:

```
project/
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── .env / .env.example
├── CLAUDE.md / AGENTS.md
│
├── docs/
│   ├── api.md
│   ├── development.md
│   └── architecture.md
│
├── scripts/
│   ├── deploy.sh
│   └── init_db.sh
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── src/
│   ├── main.py
│   ├── app.py
│   ├── config.py
│   ├── core/ (models, services, utils)
│   ├── api/ (v1/, dependencies)
│   ├── data/ (repository, migrations)
│   └── external/ (clients, integrations)
│
├── logs/
└── data/ (raw/, processed/, cache/)
```

---

### 2. Data Science / Quant Project Structure

**IF** building quant trading, ML, or AI research projects  
**THEN** use this directory structure:

```
project/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── CLAUDE.md / AGENTS.md
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
│
├── scripts/ (train_model.py, backtest.py, collect_data.py)
├── configs/ (model.yaml, database.yaml, trading.yaml)
├── tests/
│
├── src/
│   ├── data/ (collectors, processors, features, loaders)
│   ├── models/ (strategies, backtest, risk)
│   ├── utils/ (logging, database, api_client)
│   └── core/ (config, signals, portfolio)
│
├── data/ (raw/, processed/, external/, cache/)
├── models/ (checkpoints/, exports/)
└── logs/
```

---

### 3. Monorepo Structure

**IF** building microservices or large collaborative projects  
**THEN** use this directory structure:

```
project-monorepo/
├── README.md
├── LICENSE
├── .gitignore
├── docker-compose.yml
├── CLAUDE.md / AGENTS.md
│
├── docs/
├── scripts/
├── services/ (user-service/, trading-service/, data-service/)
├── assets/ (common/, repo/, database/)
├── infrastructure/ (terraform/, kubernetes/, nginx/)
└── monitoring/ (prometheus/, grafana/, alertmanager/)
```

---

### 4. Full-Stack Web Application Structure

**IF** building SPA or separated frontend/backend applications  
**THEN** use this directory structure:

```
project/
├── frontend/
│   ├── public/
│   ├── src/ (components/, pages/, store/, utils/)
│   ├── package.json
│   └── vite.config.js
│
└── backend/
    ├── requirements.txt
    ├── Dockerfile
    ├── src/ (api/, core/, models/)
    └── tests/
```

---

### 5. Core Design Principles

**IF** organizing code  
**THEN** apply Separation of Concerns: API → Service → Repository → Database

**IF** ensuring testability  
**THEN** make each module independently testable  
**THEN** use dependency injection and mocking

**IF** managing configuration  
**THEN** separate config from code  
**THEN** prefer: Environment Variables > Config Files > Defaults

**IF** setting up version control  
**THEN** add data/, logs/, models/ to .gitignore  
**THEN** only commit source code and config examples

---

### 6. Best Practices Checklist

**IF** starting a new project  
**THEN** complete these items:

- [ ] Create README.md with project overview and usage
- [ ] Create LICENSE file
- [ ] Set up virtual environment (venv/conda)
- [ ] Create requirements.txt with pinned versions
- [ ] Create .gitignore excluding sensitive files
- [ ] Create .env.example documenting required variables
- [ ] Design directory structure following SoC principles
- [ ] Set up code formatter (black)
- [ ] Set up code linter (flake8/ruff)
- [ ] Write first test case
- [ ] Initialize Git and make initial commit
- [ ] Create CHANGELOG.md

---

## Key Concept Index

| Concept | Definition |
|---------|------------|
| SoC (Separation of Concerns) | API → Service → Repository → Database |
| Monorepo | Single repo containing multiple projects/services |
| Full-Stack | Combined frontend + backend architecture |
| DRY | Don't Repeat Yourself |
| .gitignore | File specifying untracked files to ignore |
| pyproject.toml | Modern Python project configuration |
