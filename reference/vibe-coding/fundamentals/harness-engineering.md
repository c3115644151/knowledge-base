# Harness Engineering Protocol

## 适用场景
- 构建 Agent 系统和生成管线时
- 设计 Evaluation Framework 时
- 实现 Self-Optimizing 系统时

## 触发条件
- 创建 Generator → Optimizer → Evaluator 循环
- 需要提升 Agent 输出可靠性
- 设计闭环反馈系统

---

## IF-THEN Rules

### 1. Core Definition

**IF** understanding Harness Engineering  
**THEN** recognize: Harness = deterministic engineering control system that compresses LLM's non-deterministic output into predictable轨道

**IF** defining Harness purpose  
**THEN** remember: Transform "probabilistic generation" into "verifiable deliverables"

---

### 2. LLM Role Definition

**IF** integrating LLM into system  
**THEN** recognize LLM only does two things:
1. **Understand intent**
2. **Translate intent to text** (code/config/docs)

**IF** evaluating reliability  
**THEN** treat LLM as compute + language compiler, NOT reliability source

---

### 3. External Reliability Mechanisms

**IF** ensuring system reliability  
**THEN** rely on external mechanisms for four actions:

| Action | Description |
|--------|-------------|
| Intercept Intent | Validate and constrain generated intent |
| Verify Result | Check output against specifications |
| Reject Unqualified | Reject outputs that don't meet criteria |
| Inject Context | Provide necessary context proactively |

---

### 4. Minimum Viable Harness

**IF** building a minimum viable Harness  
**THEN** implement this feedback loop:

```
Generate → Compile/Run → Capture Errors → Feedback Rewrite → Until Pass
```

**IF** without this loop  
**THENEN one-time chat cannot become iterative production process

---

### 5. Hard Problem #1: Context & Forgetting

**IF** handling complex tasks  
**THEN** anticipate: Context explosion, goal drift, front/back-end mixing

**IF** solving context problems  
**THEN** implement:
- Dynamic context injection
- Memory management with pluggable skill packages
- Precise loading/unloading based on current intent
- Keep context short, accurate, relevant

---

### 6. Memory Engineering

**IF** implementing memory  
**THEN** understand: Memory ≠ "store more things"

**IF** engineering memory properly  
**THEN** automatically distill learnings into rules and沉淀  
**THEN** enable cross-task anti-error capability

---

### 7. Hard Problem #2: Self-Evaluation Hallucination

**IF** letting model evaluate its own output  
**THEN** recognize: This = athlete + referee simultaneously  
**THEN** expect: Validation + self-consistency hiding logical errors

**IF** solving self-evaluation problems  
**THEN** implement:
- Evaluation-driven development
- Mechanical testing
- Independent third-party validators (compiler, unit tests, E2E tests, QA Agent)
- Hard metrics determine pass/fail

---

### 8. Quality Lower Bound Migration

**IF** defining quality standards  
**THEN** migrate lower bound from "model intelligence" to "evaluation mechanism completeness"

**IF** measuring productivity  
**THEN** recognize: True productivity = repeatable validators, not one-time inspiration

---

### 9. Hard Problem #3: Temporal Entropy

**IF** running long-term systems  
**THEN** anticipate: Model takes shortcuts to pass tests  
**THEN** expect: Architecture drift, coupling spread, unmaintainable codebase

**IF** solving entropy problems  
**THEN** implement:
- Architecture hard constraints (block structural violations)
- Dedicated cleanup mechanism (continuous refactoring, doc updates, tech debt management)

---

### 10. Complete Harness System

**IF** building mature Harness  
**THEN** include these components:

| Component | Role |
|-----------|------|
| Planner | Defines goals and execution plans |
| Executor | Generates outputs based on plans |
| Evaluator | Validates outputs against criteria |
| Hard Constraints | Blocks structural violations |
| Cleanup Mechanism | Continuous refactoring and maintenance |

**IF** system is complete  
**THEN** it upgrades from "script" to "Agent Operating System"  
**THEN** stability comes from division and checks

---

### 11. Common Misconceptions

**IF** building AI systems  
**THEN** avoid these mistakes:

| Misconception | Reality |
|--------------|---------|
| "Model upgrade will solve deviation" | Without harness, even strongest horse pulls cart into ditch |
| "More tools are better" | Tool overload causes choice paralysis; tools should be minimal-sufficient for evaluation/execution |
| "Unconstrained vibe coding is future" | Only works in small projects without history; long-term collaboration needs hard boundaries |

---

### 12. Harness Ceiling

**IF** determining Harness upper limit  
**THEN** recognize: Ceiling = evaluator capability

**IF** unable to encode "good result" into verifiable rules/tests  
**THEN** system cannot stabilize optimization  
**THEN** model cannot complete this strategic definition

---

## Key Concept Index

| Concept | Definition |
|---------|------------|
| Harness | Deterministic control system for LLM outputs |
| Generator | Component that produces artifacts |
| Optimizer | Component that improves artifacts |
| Evaluator | Component that validates against criteria |
| Fixed Point | Stable state where system converges |
| Self-Optimizing | System that iteratively improves itself |
| Bootstrap | Process of system improving its own capabilities |
| Feedback Loop | Generate → Evaluate → Refine → Repeat |
