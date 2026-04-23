# Code Review Protocol

## 适用场景
- 对生成代码进行质量验证时
- 执行 Architecture Review 或 Release Gate 时
- 进行合规审计或 Postmortem 分析时

## 触发条件
- 完成代码生成后需要验证
- 用户请求代码审查
- 需要构建可审计的检查清单

---

## IF-THEN Rules

### Phase 1: Requirement Decomposition

**IF** given abstract requirements (y1...yn)  
**THEN** provide engineering definitions for each requirement  
**THEN** identify scope boundaries and implicit assumptions  
**THEN** list common failure modes or misunderstanding points

---

### Phase 2: Checklist Enumeration

**IF** enumerating check points  
**THEN** cover ALL of the following layers:
- Design-level check points
- Implementation-level check points
- Runtime/Ops-level check points
- Extreme/boundary/exception scenarios
- Potential conflict points with other requirements

**IF** writing check points  
**THEN** ensure each is **decidable (Yes/No/Unknown)**  
**THEN** use consistent numbering: `CP-yi-01`, `CP-yi-02`, etc.

---

### Phase 3: Step-by-Step Validation

**FOR EACH** check point, provide:
1. **Definition**: What is being verified?
2. **Necessity**: What happens if ignored?
3. **Verification Method**: Code review / test / proof / monitoring / simulation (at least one)
4. **Pass Criteria**: Clear acceptable vs unacceptable conditions (with thresholds; mark Unknown if thresholds unknown)

---

### Phase 4: System-Level Analysis

**IF** analyzing multiple requirements  
**THEN** identify:
- Conflicts (e.g., Performance vs Security)
- Strong dependencies
- Substitution relationships

**IF** conflicts exist  
**THEN** provide priority recommendations  
**THEN** provide rational decision basis (default for high-risk: Security/Compliance > Reliability > Data Correctness > Availability > Performance > Cost > Complexity)

---

## Validation Protocol

**IF** information is insufficient  
**THEN** mark all critical gaps as `Unknown`  
**THEN** provide "Minimum Viable Checklist (MVC)"  
**THEN** provide supplementary action list

**IF** conflicting requirements exist without priority info  
**THEN** explicitly list conflict pairs and causes  
**THEN** provide optional decision paths (A/B/C) with consequences

**IF** a check point cannot be binary-decided  
**THEN** reformulate as "threshold + metric + sampling window"  
**THEN** if threshold unknown, provide candidate ranges and mark Unknown

---

## Output Format

```
【Background Summary】
- Project Goal:
- Use Scenarios:
- Tech Stack/Environment:
- Key Constraints:
- Risk Level/Compliance Targets:

【Requirement-by-Requirement Output】
For each yi:
#### yi: <Requirement Name>
1. Engineering Definition
2. Scope & Boundaries
3. Complete Checkpoint List
   - CP-yi-01:
   - CP-yi-02:
4. Step-by-Step Validation
   - CP-yi-01:
     - Definition:
     - Necessity:
     - Verification Method:
     - Pass Criteria:
5. Relationship Analysis with Other Requirements

【System-Level Analysis】
- Conflicts:
- Strong Dependencies:
- Substitution Relationships:
- Priority Recommendations:
- Decision Basis:

【Audit Conclusion】
- Total Checkpoints Covered:
- Unknown Items & Supplementary Actions:
- "Is everything checked?" Determination:
```

---

## Key Concept Index

| Concept | Definition |
|---------|------------|
| CP (Checkpoint) | A verifiable test point (Yes/No/Unknown) |
| MVC (Minimum Viable Checklist) | Minimal acceptable check set when full info unavailable |
| Evidence Chain | Documentation proving requirement satisfaction |
| Control Item | A requirement mapped to verifiable checkpoints |
| Audit Trail | Traceable record from requirement to verification |
