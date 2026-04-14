# 批处理

批处理允许跨数百或数千个提示并行运行 Hermes Agent，生成结构化轨迹数据。主要用于**训练数据生成**——生成可用于微调或评估的 ShareGPT 格式轨迹。

## 快速开始

```bash
# 基本批处理运行
python batch_runner.py \
    --dataset_file=data/prompts.jsonl \
    --batch_size=10 \
    --run_name=my_first_run \
    --model=anthropic/claude-sonnet-4.6 \
    --num_workers=4

# 恢复中断的运行
python batch_runner.py \
    --dataset_file=data/prompts.jsonl \
    --batch_size=10 \
    --run_name=my_first_run \
    --resume
```

## 数据集格式

输入是 JSONL 文件（每行一个 JSON 对象）。每个条目必须有 `prompt` 字段：

```json
{"prompt": "Write a Python function that finds the longest palindromic substring"}
{"prompt": "Create a REST API endpoint for user authentication using Flask"}
```

可选字段：
- `image` 或 `docker_image`：容器镜像
- `cwd`：工作目录覆盖

## 配置选项

| 参数 | 默认 | 描述 |
|------|------|------|
| `--dataset_file` | (必需) | JSONL 数据集路径 |
| `--batch_size` | (必需) | 每批提示数 |
| `--run_name` | (必需) | 运行名称（用于输出目录） |
| `--model` | `claude-sonnet-4.6` | 使用的模型 |
| `--num_workers` | `4` | 并行工作进程数 |
| `--max_turns` | `10` | 每提示最大工具调用迭代 |
| `--resume` | `false` | 从检查点恢复 |
| `--distribution` | `"default"` | 工具集分发采样 |

### 提供商路由 (OpenRouter)

| 参数 | 描述 |
|------|------|
| `--providers_allowed` | 允许的提供商逗号分隔列表 |
| `--providers_ignored` | 忽略的提供商逗号分隔列表 |
| `--providers_order` | 首选提供商顺序 |
| `--provider_sort` | 排序方式：`"price"`、`"throughput"` 或 `"latency"` |

## 输出格式

所有输出到 `data/<run_name>/`：

```
data/my_run/
├── trajectories.jsonl  # 合并最终输出
├── batch_0.jsonl      # 单批结果
├── checkpoint.json    # 恢复检查点
└── statistics.json   # 聚合工具使用统计
```

### 轨迹格式

```json
{
  "prompt_index": 42,
  "conversations": [
    {"from": "human", "value": "Write a function..."},
    {"from": "gpt", "value": "I'll create...", "tool_calls": [...]},
    {"from": "tool", "value": "..."},
    {"from": "gpt", "value": "Here's the completed function..."}
  ],
  "metadata": {
    "batch_num": 2,
    "timestamp": "2026-01-15T10:30:00",
    "model": "anthropic/claude-sonnet-4.6"
  },
  "completed": true,
  "toolsets_used": ["terminal", "file"],
  "tool_stats": {
    "terminal": {"count": 2, "success": 2, "failure": 0},
    "read_file": {"count": 1, "success": 1, "failure": 0}
  }
}
```

## 检查点

- **检查点文件**：每批完成后保存
- **基于内容的恢复**：运行时通过实际文本内容匹配已完成提示（不仅是索引）
- **失败提示**：只有成功完成的提示标记为完成

## 质量过滤

- **无推理过滤**：零推理轮次的样本被丢弃
- **损坏条目过滤**：幻觉工具名称的条目被过滤
- **推理统计**：跟踪整个运行中带/不带推理的轮次百分比

## 统计

完成后，打印综合统计：
- **工具使用**：每工具调用计数、成功/失败率
- **推理覆盖**：带推理的助手轮次百分比
- **丢弃样本**：因缺乏推理而过滤的样本数
- **持续时间**：总处理时间
