# Gemini 无头模式 JSONL 规范化 - 配置协议

## 前置条件检查清单

- [ ] 本地已安装 Gemini CLI (`gemini-2.5-flash`)
- [ ] 系统已配置 `gemini` 命令行工具
- [ ] 具备网络访问能力（可设置 `http_proxy/https_proxy`）
- [ ] 待处理的 `.md` 提示词文件位于目标目录
- [ ] 具备 Shell 脚本执行环境（Bash）

## 配置步骤（IF-THEN）

### 步骤 1：准备工作

```
IF 需要处理单文件
THEN 执行单文件转换命令
```

```bash
# 设置系统提示词（JSONL 转换器）
SYS_PROMPT_JSONL=$(cat <<'EOF'
{"category_id": 1, "category": "JSONL规范化", "row": 2, "col": 1, "title": "# JSONL 提示词转换器 - 系统提示词", "content": "..."}
EOF
)

# 单条转换（stdin 输入提示词内容，stdout 得到单行 JSON）
cat <输入文件> | gemini -m gemini-2.5-flash \
  --output-format text \
  --allowed-tools '' \
  "$SYS_PROMPT_JSONL"
```

### 步骤 2：批量处理目录

```
IF 需要批量转换目录下所有 .md 文件
THEN 执行批量处理脚本
```

```bash
SYS_PROMPT_JSONL=... # 同步骤1
out=2/prompts.jsonl
: > "$out"
for f in 2/*.md; do
  [ -f "$f" ] || continue
  cat "$f" | gemini -m gemini-2.5-flash \
    --output-format text \
    --allowed-tools '' \
    "$SYS_PROMPT_JSONL" >> "$out"
done
```

### 步骤 3：代理配置（如需要）

```
IF 网络需要通过代理访问
THEN 在命令前设置代理环境变量
```

```bash
export http_proxy=http://<proxy-host>:<port>
export https_proxy=http://<proxy-host>:<port>
# 然后执行步骤1或步骤2
```

## 验证检查点

- [ ] 每行输出是合法 JSON 对象
- [ ] 对象包含 `title` 与 `content` 两个字段
- [ ] 无额外解释、空行或代码块定界符
- [ ] `title` 取自首个 `#` 标题或前50字符
- [ ] 换行符、引号、反斜杠已正确转义（`\\n` / `\\"` / `\\\\`）
- [ ] `wc -l prompts.jsonl` 行数等于处理文件数
- [ ] 随机抽查2-3行确认转义正确

## 常见故障

| 问题 | 解决方案 |
|------|----------|
| 输出混入CLI提示或日志 | 确保未开启 `--debug`，避免循环内打印stdout |
| 代理导致失败 | 移除代理或改用本地直连后重试 |
| 行数不匹配 | 检查循环是否包含 `*.jsonl` 自身或隐藏文件 |
