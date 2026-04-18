# Knowledge Base

结构化知识沉淀与检索。

## 结构

```
知识库/
├── reference/              # AI 专用参考文档（批量生成）
│   ├── neoForge/          # NeoForge API 文档（53 个）
│   └── hermes/            # Hermes Agent 文档（72 个）
├── topics/                 # 个性化知识（交流沉淀）
│   └── books/             # 读书笔记（5 本）
├── raw/                    # 原料知识（待加工）
├── index.md               # 全局索引
└── log.md                 # 操作日志
```

## 三类知识

### reference/ - AI 参考文档

工具书性质。批量生成，结构固定，查阅型。

当前内容：
- **NeoForge 开发文档**（53 个）
  - 版本：NeoForge 26.1.x / Minecraft 1.21.11
  - 来源：https://docs.neoforged.net
- **Hermes Agent 文档**（72 个）
  - 开源 AI Agent，MIT 许可证
  - 来源：https://hermes-agent.nousresearch.com

### topics/ - 个性化知识

日记本性质。交流沉淀，结构灵活，演进型。

- **NeoForge 开发认知** - 版本规范、构建配置
- **读书笔记**（5 本）- 投资心理学、人群行为、哲学

### raw/ - 原料知识

待加工的原始素材。如股票基础概念、视频解析结果等。

## 设计原则

**知识集中**。同一话题只维护一个笔记，随时间演进。

**知识可追溯**。记录来源，才能验证。

**知识可碰撞**。新知识与旧知识对话，才能生长。

## 同步

每 3 天自动整理并推送到 GitHub。
