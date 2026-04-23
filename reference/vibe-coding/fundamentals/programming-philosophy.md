# Programming Philosophy Protocol

## 适用场景
- 理解编程本质和抽象层次时
- 做出架构设计决策时
- 追求代码长期可维护性时

## 触发条件
- 设计新的系统或模块
- 面临复杂代码或重构任务
- 需要在多种实现方案中做选择

---

## IF-THEN Rules

### 1. Program Ontology

**IF** understanding what a program is  
**THEN** recognize: Program = Data + Functions
- Data = facts (existence)
- Functions = intentions (change)

**IF** analyzing program behavior  
**THEN** trace: Input → Processing → Output  
**THEN** recognize that state determines world form, transforms describe process

---

### 2. Three Cores: Data · Function · Abstraction

**IF** working with data  
**THEN** remember: Data structure = thought structure  
**IF** data is clear, program follows naturally

**IF** writing functions  
**THEN** ensure logic is transformation, not manipulation  
**THEN** follow: Process = cause and effect

**IF** creating abstractions  
**THEN** remove noise, preserve essence  
**THEN** hide unnecessary details, expose necessary ones

---

### 3. Paradigm Evolution

**IF** choosing programming paradigm  
**THEN** consider the evolution: Imperative → Declarative → Intentional

| Paradigm | World View | Focus |
|----------|------------|-------|
| Procedural | World = steps | Control flow |
| Object-Oriented | World = things | State + behavior |
| Intentional | World = intentions | Requirements |

---

### 4. Design Principles

**IF** designing modules  
**THEN** apply High Cohesion: related things stay together, unrelated things stay apart

**IF** managing dependencies  
**THEN** apply Low Coupling: modules are like planets—predictable but not bound

---

### 5. System Perspective

**IF** viewing code as a system  
**THEN** apply:
- **State**: All errors stem from improper state; fewer states = more stability
- **Transform**: All systems = `output = transform(input)`
- **Composability**: Small units → composable → reusable → evolvable

---

### 6. Declarative vs Imperative

**IF** writing high-level code  
**THEN** prefer declarative (tell WHAT, not HOW)  
**IF** writing low-level code  
**THEN** imperative is acceptable

**IF** designing  
**THEN** follow: Spec first, then implementation  
**THEN** follow: Behavior → Structure → Code

---

### 7. Stability & Evolution

**IF** designing interfaces  
**THEN** keep interfaces stable, implementations flexible  
**THEN** remember: Breaking interface = breaking trust

**IF** managing complexity  
**THEN** remember: Complexity doesn't disappear, it transfers  
**THEN** decide who bears the complexity (you or user)

---

### 8. Predictability

**IF** evaluating code quality  
**THEN** prioritize predictability over performance  
**THEN** ensure code can be reasoned by human brain  
**THEN** apply: fewer variables, shallow branches, clear state, flat logic

---

### 9. Time Perspective

**IF** designing logic  
**THEN** recognize program = temporal structure (not spatial)  
**THEN** answer three questions:
1. Who holds the state?
2. When does state change?
3. Who triggers the change?

---

### 10. API Philosophy

**IF** designing interfaces  
**THEN** remember: API is a language, language shapes thought  
**THEN** design until misuse becomes impossible

**IF** maintaining compatibility  
**THEN** treat backward compatibility as responsibility

---

### 11. Errors & Invariants

**IF** handling errors  
**THEN** assume errors are normal (correctness needs proof)  
**IF** maintaining stability  
**THEN** preserve invariants (program's physical laws)

---

### 12. Evolvability

**IF** writing code  
**THEN** remember: Software is ecology, not sculpture  
**THEN** write code your future self can understand

---

## Key Concept Index

| Concept | Definition |
|---------|------------|
| Data | Facts/existence in a program |
| Function | Intent/change in a program |
| Abstraction | Essence extraction, hiding complexity |
| Cohesion | Related code stays together |
| Coupling | Dependency degree between modules |
| Invariant | Condition that must always hold true |
| Declarative | State WHAT, not HOW |
| Composable | Units that can combine into larger systems |
