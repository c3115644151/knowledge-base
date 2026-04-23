# Code Organization Protocol

## 适用场景
- 规划新项目结构时
- 组织代码模块和文件时
- 编写文档和 README 时

## 触发条件
- 创建新项目或新模块
- 需要决定文件放置位置
- 编写代码注释或文档字符串

---

## IF-THEN Rules

### 1. Modular Programming

**IF** writing code  
**THEN** divide into small, reusable modules or functions  
**THEN** ensure each module handles only one responsibility (Single Responsibility)

**IF** organizing project structure  
**THEN** use explicit module structure and directories  
**THEN** make code easy to navigate

---

### 2. Naming Conventions

**IF** naming files  
**THEN** use lowercase_with_underscores or camelCase  
**THEN** make names reflect content responsibility  
**THEN** avoid vague abbreviations

**IF** naming variables and functions  
**THEN** use meaningful, consistent conventions:
- Classes: CamelCase (e.g., `UserProfile`)
- Functions/variables: snake_case (e.g., `get_user_age`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_RETRY_COUNT`)

**IF** naming functions  
**THEN** use verbs (e.g., `calculate`, `fetch`, `process`)  
**IF** naming variables  
**THEN** use nouns (e.g., `user_age`, `order_list`)

---

### 3. Code Comments

**IF** adding comments to complex code  
**THEN** explain the code's purpose and logic  
**THEN** use block comments (`/*...*/`) for multi-line explanations  
**THEN** use line comments (`//` or `#`) for inline notes

**IF** writing docstrings  
**THEN** include: module/class/function purpose, parameters, return values  
**THEN** choose a consistent format: Google Style, NumPy/SciPy Style, or Sphinx Style

---

### 4. Code Formatting

**IF** formatting code  
**THEN** use consistent style and rules  
**THEN** use automated tools (Prettier, Black, ESLint, Pylint)  
**THEN** apply proper indentation, spacing, and blank lines for readability

---

### 5. Documentation

**IF** writing README files  
**THEN** include: project purpose, installation, usage, examples  
**THEN** use Markdown syntax for easy reading and maintenance

**IF** generating documentation  
**THEN** use tools like Sphinx, Doxygen, or JSDoc  
**THEN** keep documentation synchronized with code

---

### 6. IDE Configuration

**IF** using an IDE  
**THEN** configure linter plugins (ESLint, Pylint)  
**THEN** enable code formatting tools  
**THEN** leverage autocomplete, error checking, and debugging features

---

## Key Concept Index

| Concept | Definition |
|---------|------------|
| Single Responsibility | Each module/function does exactly one thing |
| DRY (Don't Repeat Yourself) | Extract common logic to reusable units |
| Semantic Naming | Names describe purpose, not implementation |
| Docstring | Inline documentation for modules/classes/functions |
| Linter | Tool that analyzes code for style/quality issues |
| Formatter | Tool that standardizes code style (Prettier, Black) |
| Markdown | Lightweight markup language for documentation |
