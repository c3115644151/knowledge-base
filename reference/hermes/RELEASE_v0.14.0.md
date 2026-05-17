# v0.14.0 (2026.5.16)

> Hermes Agent CLI v0.14.0 发布

---

## 🚨 安全修复

- **CVE 依赖更新** - 升级 aiohttp、anthropic、cryptography 至 CVE 修复版本 ([#26830](https://github.com/nousresearch/hermes-agent/pull/26830))
- **OAuth PKCE 分离** - 将 OAuth PKCE state 与 code_verifier 正确分离 ([#26829](https://github.com/nousresearch/hermes-agent/pull/26829))
- **工具错误字符串清理** - 在注入模型上下文前清理工具错误字符串 ([#26823](https://github.com/nousresearch/hermes-agent/pull/26823))

---

## 🔍 X (Twitter) 搜索工具

- **gated X Search 工具** - 支持 OAuth 或 API-key 认证 ([#26763](https://github.com/nousresearch/hermes-agent/pull/26763))
- **xAI OAuth 改进** - 修复 entitlement-403 提示、增加 grok-4.3 上下文至 1M ([#26664](https://github.com/nousresearch/hermes-agent/pull/26664))

---

## 📹 视频生成工具

- **video_generate / video_gen 文档** - 新增用户面向的工具文档 ([#27050](https://github.com/nousresearch/hermes-agent/pull/27050))

---

## 🛠️ CLI 改进

- **`hermes send` 命令** - 将脚本输出管道到任意消息平台 ([#27188](https://github.com/nousresearch/hermes-agent/pull/27188))
- **`/exit --delete` 标志** - 退出时删除 session ([#27101](https://github.com/nousresearch/hermes-agent/pull/27101))
- **`/status` 增强** - 追加 session recap 输出 ([#27176](https://github.com/nousresearch/hermes-agent/pull/27176))
- **后台任务指示器** - 状态栏显示 ▶ N 指示器 ([#27175](https://github.com/nousresearch/hermes-agent/pull/27175))

---

## 🔧 插件系统

- **工具覆盖标志** - 支持替换内置工具 ([#26759](https://github.com/nousresearch/hermes-agent/pull/26759))
- **category-namespaced 插件** - 在 hermes plugins 列表中正确显示 ([#27105](https://github.com/nousresearch/hermes-agent/pull/27105))
- **MCP 并行工具调用** - 支持 `supports_parallel_tool_calls` ([#26825](https://github.com/nousresearch/hermes-agent/pull/26825))

---

## 📦 新技能 (Optional Skills)

- **osint-investigation** - 新增 OSINT 调查技能 ([#26729](https://github.com/nousresearch/hermes-agent/pull/26729))
- **darwinian-evolver** - 新增达尔文进化技能 ([相关 PR](https://github.com/nousresearch/hermes-agent/pull/26699))
- **pinggy-tunnel** - 新增 pinggy tunnel 技能 ([相关 PR](https://github.com/nousresearch/hermes-agent/pull/26712))

---

## 🐛 修复

| 组件 | 修复内容 |
|:---|:---|
| **Telegram** | 恢复 DM topic typing indicator |
| **Signal** | 正确读取 groupV2.id |
| **xAI** | 流式推理边界恢复、entitlement 403 处理 |
| **Gateway** | 合并活跃会话中的快速 TEXT 跟进 |
| **ACP** | session/load 前重放会话历史 |
| **DeepSeek** | thinking.type + reasoning_effort 映射 |
| **MCP** | 远程 URL 前置验证 |
| **Moonshot** | 工具 schema 中的 $ref 清理 |
| **Windows** | 修复 Tirth 不可用警告、TOCTOU 竞态 |
| **TUI** | Ink displayCursor 同步、Markdown 表格渲染 |

---

## 📚 文档更新

- **Programmatic Integration 概览** - 新增集成指南
- **pip 安装路径** - 添加到安装、快速开始、更新和 CLI 参考
- **v0.14.0 Highlights** - 重写发布亮点，提升可读性
- **Notion 技能重构** - 适配 Notion 开发者平台 (2026年5月)

---

## 贡献者

感谢 @worlldz 等贡献者！
