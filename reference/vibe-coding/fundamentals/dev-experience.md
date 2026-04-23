# Dev Experience Protocol

## 适用场景
- Agent 参与实际项目开发时
- 需要遵循项目规范和组织原则时
- 构建新项目或维护现有代码库时

## 触发条件
- 用户请求创建新文件或模块
- 需要理解项目结构或代码规范
- 涉及变量命名、文件组织或编码标准时

---

## IF-THEN Rules

### 1. Variable Naming

**IF** creating a new variable  
**THEN** maintain a centralized variable index file with columns: `name | description | location | frequency`

**IF** naming variables  
**THEN** use semantic, English-compliant names  
**THEN** use `CONSTANT_NAME` for constants  
**THEN** avoid single letters (`a`, `b`, `c`) or unclear abbreviations

---

### 2. File Structure & Naming

**IF** organizing code files  
**THEN** follow lowercase_with_underscores or camelCase conventions  
**THEN** include subdirectories containing:
- `agents/` for automation logic and prompts
- `claude.md` for folder documentation

**IF** naming files  
**THEN** make names reflect their responsibility  
**THEN** avoid abbreviations that reduce clarity

---

### 3. Coding Standards

**IF** writing functions, classes, or modules  
**THEN** apply Single Responsibility Principle (one unit does one thing)

**IF** encountering duplicated logic  
**THEN** extract into reusable components (DRY principle)

**IF** designing system behavior  
**THEN** clearly separate:
- Consumer: receives external data
- Producer: generates output
- State (variables): stores system information
- Transform (functions): processes data

**IF** handling concurrency  
**THEN** clearly identify shared resources  
**THEN** use locks or thread-safe structures when necessary

---

### 4. Architecture Principles

**IF** starting a new project  
**THEN** first clarify: module boundaries, I/O, data flow, service boundaries, tech stack, dependencies

**IF** developing code  
**THEN** follow: Understand Requirements → Keep Simple → Write Tests → Iterate Small

---

### 5. Core Programming Philosophy

**IF** approaching any problem  
**THEN** start from the problem, not from code

**IF** facing complex problems  
**THEN** apply Divide & Conquer (break into solvable units)

**IF** writing code  
**THEN** follow KISS (Keep It Simple, Stupid)  
**THEN** follow DRY (Don't Repeat Yourself)  
**THEN** prioritize readability over cleverness

**IF** adding comments  
**THEN** explain WHY, not HOW

**IF** developing features  
**THEN** follow: Make it work → Make it right → Make it fast

**IF** debugging errors  
**THEN** read error messages, check logs, trace issues layer by layer (this is a core skill)

---

### 6. Version Control

**IF** working on any project  
**THEN** use Git for version control  
**THEN** never keep code only locally

**IF** writing code  
**THEN** write maintainable automated tests

---

## Key Concept Index

| Concept | Definition |
|--------|------------|
| DRY | Don't Repeat Yourself - reuse logic via functions/classes/modules |
| KISS | Keep It Simple, Stupid - reduce complexity and magic |
| Single Responsibility | Each unit (file/class/function) does one thing |
| Semantic Naming | Names reflect purpose, not implementation |
| Divide & Conquer | Break complex problems into independent smaller units |
| Layered Architecture | UI → Service → Repository → Database |
| Microservices | Independent services for independent deployment/scaling |
| Redis | Caching layer for read performance, reducing DB load |
| Message Queue | Async communication between services (decoupling, buffering) |
