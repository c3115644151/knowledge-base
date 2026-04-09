# NeoForge 服务端资源

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/server/

## 概述

服务端资源包括配方、战利品表、标签、进度等数据驱动的游戏内容。

## 子主题

- [进度系统](./NeoForge-服务端-进度.md)
- [伤害类型](./NeoForge-服务端-伤害类型.md)
- [数据映射](./NeoForge-服务端-数据映射.md)
- [附魔系统](./NeoForge-服务端-附魔.md)
- [战利品表](./NeoForge-服务端-战利品表.md)
- [配方系统](./NeoForge-服务端-配方.md)
- [标签系统](./NeoForge-服务端-标签.md)

## 数据文件位置

```
data/<namespace>/
├── advancements/           # 进度
├── loot_tables/            # 战利品表
│   ├── blocks/
│   ├── entities/
│   └── chests/
├── recipes/                # 配方
├── tags/                   # 标签
│   ├── blocks/
│   ├── entity_types/
│   ├── fluids/
│   ├── functions/
│   ├── items/
│   └── worldgen/
└── worldgen/              # 世界生成
```

---

## 关联引用

- 客户端资源：[NeoForge-客户端资源](./NeoForge-客户端资源.md)
- 数据生成：[NeoForge-数据生成](./NeoForge-数据生成.md)
