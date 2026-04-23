# 导入和导出

> **核心摘要**: CLI 命令支持在 Paperclip 公司格式和可移植文件夹包之间导入导出。

## 导出公司

将公司导出为可移植文件夹包（包含清单和 markdown 文件）：

```bash
pnpm paperclipai company export <company-id> --out ./exports/acme --include company,agents
```

## 预览导入

预览导入（无写入）：

```bash
pnpm paperclipai company import \
  <owner>/<repo>/<path> \
  --target existing \
  --company-id <company-id> \
  --ref main \
  --collision rename \
  --dry-run
```

## 应用导入

应用导入：

```bash
pnpm paperclipai company import \
  ./exports/acme \
  --target new \
  --new-company-name "Acme Imported" \
  --include company,agents
```

## 导入选项

| 选项 | 说明 |
|------|------|
| `--target` | `new`（新公司）或 `existing`（现有公司） |
| `--collision` | 冲突处理：`rename`、`skip`、`overwrite` |
| `--include` | 包含哪些内容：`company`、`agents`、`goals`、`projects` |
| `--ref` | Git 分支或 commit SHA |
