# RL 训练

Hermes Agent 包含基于 **Tinker-Atropos** 的集成强化学习（RL）训练管道，支持使用 GRPO（Group Relative Policy Optimization）和 LoRA 适配器训练语言模型。

## 概述

RL 训练系统由三个组件构成：

1. **Atropos** — 轨迹 API 服务器，协调环境交互、管理 rollout 组、计算优势
2. **Tinker** — 训练服务，处理模型权重、LoRA 训练、采样/推理、优化器步骤
3. **Environments** — Python 类，定义任务、评分和奖励函数（如 GSM8K 数学问题）

## 需求

- **Python >= 3.11**
- **TINKER_API_KEY** — Tinker 训练服务 API 密钥
- **WANDB_API_KEY** — Weights & Biases 指标追踪
- `tinker-atropos` 子模块

```bash
hermes config set TINKER_API_KEY your-tinker-key
hermes config set WANDB_API_KEY your-wandb-key
```

## 可用工具

| 工具 | 描述 |
|------|------|
| `rl_list_environments` | 发现可用的 RL 环境 |
| `rl_select_environment` | 选择环境并加载配置 |
| `rl_get_current_config` | 查看可配置和锁定字段 |
| `rl_edit_config` | 修改可配置训练参数 |
| `rl_start_training` | 启动训练（生成 3 个进程） |
| `rl_check_status` | 监控训练进度和 WandB 指标 |
| `rl_stop_training` | 停止运行中的训练任务 |
| `rl_get_results` | 获取最终指标和模型权重路径 |
| `rl_list_runs` | 列出所有活动/完成的运行 |
| `rl_test_inference` | 使用 OpenRouter 快速推理测试 |

## 工作流

### 1. 发现环境

```bash
# 列出可用的 RL 环境
```

调用 `rl_list_environments()` 扫描 `tinker-atropos/tinker_atropos/environments/`。

### 2. 选择和配置

```bash
# 选择 GSM8K 环境并显示配置
```

可配置字段：`group_size`、`batch_size`、`wandb_name`
锁定字段：`tokenizer_name`、`lora_rank`、`learning_rate`、`total_steps`

### 3. 启动训练

调用 `rl_start_training()` 会：
1. 生成 YAML 配置文件
2. 创建唯一运行 ID
3. 生成三个进程：Atropos API → Tinker trainer → Environment

### 4. 监控进度

调用 `rl_check_status(run_id)` 报告：
- 进程状态（运行/退出）
- 运行时间
- WandB 指标（step、reward_mean、percent_correct）
- 日志文件位置

### 5. 停止或获取结果

- `rl_stop_training()` — 按反向顺序终止三个进程
- `rl_get_results()` — 检索最终 WandB 指标

## 推理测试

使用 `rl_test_inference` 可在提交完整训练前测试环境是否正常工作。默认：
- 3 步 × 16 completions = 48 rollouts/模型
- 测试 3 个不同规模的模型

## WandB 指标

| 指标 | 描述 |
|------|------|
| `train/loss` | 训练损失（重要性采样） |
| `train/learning_rate` | 当前学习率 |
| `reward/mean` | 组间平均奖励 |
| `logprobs/diff` | 对数概率漂移 |
| `advantages/mean` | 平均优势值 |

## 日志文件

每个训练运行在 `~/.hermes/logs/rl_training/` 生成日志：
```
logs/
├── api_{run_id}.log    # Atropos API 服务器日志
├── trainer_{run_id}.log # Tinker 训练器日志
├── env_{run_id}.log    # 环境进程日志
└── inference_tests/     # 推理测试结果
```

## 创建自定义环境

1. 在 `tinker-atropos/tinker_atropos/environments/` 创建 Python 文件
2. 定义继承自 `BaseEnv` 的类
3. 实现必需方法：`load_dataset()`、`get_next_item()`、`score_answer()`、`collect_trajectories()`
