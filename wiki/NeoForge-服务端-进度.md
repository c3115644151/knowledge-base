# NeoForge 进度系统

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/server/advancements

## 概述

进度（Advancements）系统用于追踪玩家成就和触发奖励。

## 文件位置

```
data/<namespace>/advancements/<path>.json
```

---

## 代码示例

### 基本进度

```json
{
    "display": {
        "title": "My First Achievement",
        "description": "Craft my first item",
        "icon": {
            "item": "examplemod:custom_item"
        },
        "frame": "task",
        "show_toast": true,
        "announce_to_chat": true
    },
    "criteria": {
        "tick": {
            "trigger": "minecraft:tick"
        }
    }
}
```

### 带条件的进度

```json
{
    "display": {
        "title": "Diamond Collector",
        "icon": {
            "item": "minecraft:diamond"
        }
    },
    "parent": "examplemod:root",
    "criteria": {
        "has_diamond": {
            "trigger": "minecraft:inventory_changed",
            "conditions": {
                "items": [
                    {
                        "items": ["minecraft:diamond"]
                    }
                ]
            }
        }
    }
}
```

---

## 关联引用

- 配方系统：[NeoForge-服务端-配方](./NeoForge-服务端-配方.md)
