# Telegram Bot 开发项目

## 项目背景

Telegram Bot 开发实战项目，涉及消息格式处理、Markdown 渲染问题排查与修复。主要解决 Bot 在发送格式化消息时遇到的解析错误。

## 核心技术栈

- **语言**: Python
- **框架**: python-telegram-bot
- **平台**: Telegram Bot API

## 关键实现要点

### IF-THEN 规则

1. **IF** 使用字符串拼接方式构建 Markdown 代码块
   **THEN** 在 ``` 后加了 `\n`，导致 Telegram Markdown 解析器无法识别代码块边界

2. **IF** 使用三引号字符串（triple-quoted string）构建 Markdown 代码块
   **THEN** 确保 ``` 单独成行，Markdown 格式正确解析

## 遇到的问题与解决方案

### 问题描述

```
❌ 排盘失败: Can't parse entities: can't find end of the entity starting at byte offset 168
```

### 根因分析

`bot.py` 中 `header` 消息的 Markdown 代码块格式错误。字符串拼接方式导致代码块边界不清晰。

### 修复方案

```python
# 错误写法
header = (
    "```\n"
    f"{filename}\n"
    "```\n"
)

# 正确写法
header = f"""报告见附件
```{filename}
{ai_filename}
```
"""
```

## 可复用经验总结

1. **Markdown 格式陷阱**：Telegram Markdown 对格式要求严格，代码块必须单独成行
2. **三引号字符串**：Python 中构建多行字符串时，优先使用三引号避免转义问题
3. **调试信息捕获**：错误信息中的 byte offset 可用于定位问题代码位置

---

**源文档**: `/tmp/vibe-coding-cn/assets/documents/case-studies/telegram-dev/`
