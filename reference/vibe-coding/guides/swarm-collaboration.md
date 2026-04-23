# AI 蜂群协作系统 (AI Swarm Collaboration)

> **系统类型**：多 AI Agent 协作框架
> **核心工具**：tmux
> **AI 执行要点**：让多个 AI 互相感知、通讯、控制

---

## 一、核心思想

```
传统模式：
├─ 人 ←→ AI₁
├─ 人 ←→ AI₂
└─ 人 ←→ AI₃
问题：人是瓶颈

蜂群模式：
├─ 人 → AI₁ ←→ AI₂ ←→ AI₃
└─ AI 自主协作
```

---

## 二、核心能力

| 能力 | tmux 命令 | 效果 |
|:---|:---|:---|
| 感知 | `capture-pane` | 读取任意终端内容 |
| 控制 | `send-keys` | 向任意终端发送按键 |
| 协调 | 共享状态文件 | 任务同步与分工 |

---

## 三、协作模式

### 3.1 对等模式 (P2P)

```
┌─────┐     ┌─────┐
│ AI₁ │◄───►│ AI₂ │
└──┬──┘     └──┬──┘
   │           │
   ▼           ▼
┌─────┐     ┌─────┐
│ AI₃ │◄───►│ AI₄ │
└─────┘     └─────┘

特点：所有 AI 平等，互相监控
适用：简单任务，无明确依赖
```

### 3.2 主从模式 (Master-Worker)

```
        ┌──────────┐
        │ AI-Master│
        │  (指挥官) │
        └────┬─────┘
             │ 分发/监控
    ┌────────┼────────┐
    ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐
│Worker│ │Worker│ │Worker│
│ AI-1 │ │ AI-2 │ │ AI-3 │
└──────┘ └──────┘ └──────┘

特点：一个指挥，多个执行
适用：复杂项目，需要统一协调
```

### 3.3 流水线模式 (Pipeline)

```
┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐
│ AI₁ │───►│ AI₂ │───►│ AI₃ │───►│ AI₄ │
│分析 │    │设计 │    │实现 │    │测试 │
└─────┘    └─────┘    └─────┘    └─────┘

特点：任务串行流转
适用：有明确阶段的工作流
```

---

## 四、命令速查

### 4.1 信息获取

```bash
# 列出所有会话
tmux list-sessions

# 列出所有窗口
tmux list-windows -a

# 列出所有窗格
tmux list-panes -a

# 获取当前窗口标识
echo $TMUX_PANE
```

### 4.2 内容读取

```bash
# 读取指定窗口内容（最近 N 行）
tmux capture-pane -t <session>:<window> -p -S -<N>

# 示例：读取会话 0 窗口 1 最近 100 行
tmux capture-pane -t 0:1 -p -S -100
```

### 4.3 发送控制

```bash
# 发送文本 + 回车
tmux send-keys -t 0:1 "ls -la" Enter

# 发送确认
tmux send-keys -t 0:1 "y" Enter

# 发送 Ctrl+C
tmux send-keys -t 0:1 C-c
```

---

## 五、协作协议

### 5.1 状态定义

```
状态文件位置：/tmp/ai_swarm/

状态日志格式：
[HH:MM:SS] [窗口ID] [状态] 描述

状态类型：
├─ [START]  - 开始任务
├─ [DONE]   - 完成任务
├─ [WAIT]   - 等待中
├─ [ERROR]  - 出现错误
├─ [HELP]   - 请求帮助
└─ [SKIP]   - 跳过（已有人处理）
```

### 5.2 协作规则

| 规则 | 描述 | 实现 |
|:---|:---|:---|
| 先查后做 | 开始前扫描其他终端 | `capture-pane` 全扫 |
| 避免冲突 | 相同任务不重复执行 | 检查 locks 目录 |
| 主动救援 | 发现卡住主动帮助 | 检测 `[y/n]` 等待 |
| 状态广播 | 完成后通知其他 AI | 写入 status.log |

---

## 六、AI 执行流程

```
FUNCTION swarm_collaborate(任务)
  │
  ├─► 1. 扫描环境
  │     └─► for w in $(tmux list-windows -a); do
  │           echo "=== $w ==="
  │           tmux capture-pane -t "$w" -p -S -20
  │         done
  │
  ├─► 2. 检查锁
  │     └─► if [ ! -f /tmp/ai_swarm/locks/task.lock ]; then
  │           echo "$TMUX_PANE" > /tmp/ai_swarm/locks/task.lock
  │         fi
  │
  ├─► 3. 执行任务
  │     └─► [执行具体任务]
  │
  ├─► 4. 状态广播
  │     └─► echo "[$(date +%H:%M:%S)] [$TMUX_PANE] [DONE] <描述>" >> /tmp/ai_swarm/status.log
  │
  └─► 5. 释放锁
        └─► rm /tmp/ai_swarm/locks/task.lock

END FUNCTION
```

---

## 七、异常检测

```
IF 发现以下模式 THEN 介入
  ├─ "[y/n]" / "[Y/n]" / "确认" → 需要确认
  ├─ "Error" / "Failed" / "Exception" → 出现错误
  ├─ "Waiting" / "Blocked" → 任务阻塞
  └─ 长时间无输出 → 可能卡死

干预方式：
├─ 帮助确认：tmux send-keys -t <窗口> "y" Enter
├─ 中断错误：tmux send-keys -t <窗口> C-c
└─ 发送指令：tmux send-keys -t <窗口> "<指令>" Enter
```

---

## 八、初始化流程

```bash
# 1. 创建共享目录
mkdir -p /tmp/ai_swarm/{locks,results}
touch /tmp/ai_swarm/status.log

# 2. 开启 tmux 会话
tmux new-session -d -s ai

# 3. 创建多个窗口
tmux new-window -t ai -n "master"
tmux new-window -t ai -n "worker-1"
tmux new-window -t ai -n "worker-2"

# 4. 在每个窗口启动 AI
tmux send-keys -t ai:master "claude" Enter
tmux send-keys -t ai:worker-1 "claude" Enter
```

---

**系统版本**：v1.0
**来源**：tukuaiai/vibe-coding-cn
