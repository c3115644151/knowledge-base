# 内置工具参考

本文档记录 Hermes 工具注册表中的所有 47 个内置工具，按工具集分组。**快速统计**：10 个浏览器工具、4 个文件工具、10 个 RL 工具、4 个 Home Assistant 工具、2 个终端工具、2 个网页工具，以及其他工具集中的 15 个独立工具。

## `browser` 工具集

| 工具 | 描述 | 需求环境 |
|------|------|----------|
| `browser_back` | 在浏览器历史中导航回上一页面 |
| `browser_click` | 点击快照中元素（ref ID 如 `@e5`） |
| `browser_console` | 获取浏览器控制台输出和 JavaScript 错误 |
| `browser_get_images` | 获取页面上所有图片 URL 和 alt 文本 |
| `browser_navigate` | 导航到 URL，初始化会话并加载页面 |
| `browser_press` | 按键盘键（Enter 提交表单，Tab 导航） |
| `browser_scroll` | 滚动页面 |
| `browser_snapshot` | 获取页面文本快照，返回交互元素 ref ID |
| `browser_type` | 在输入字段输入文本 |
| `browser_vision` | 截屏并用视觉 AI 分析 |

## `clarify` 工具集

| 工具 | 描述 |
|------|------|
| `clarify` | 需要澄清、反馈或决定时向用户提问。支持多选（最多 4 选项）或开放式问题 |

## `code_execution` 工具集

| 工具 | 描述 |
|------|------|
| `execute_code` | 运行可编程调用 Hermes 工具的 Python 脚本。用于 3+ 工具调用且需要处理逻辑、条件分支等场景 |

## `cronjob` 工具集

| 工具 | 描述 |
|------|------|
| `cronjob` | 统一计划任务管理器。使用 `action="create"`, `"list"`, `"update"`, `"pause"`, `"resume"`, `"run"`, `"remove"` 管理作业 |

## `delegation` 工具集

| 工具 | 描述 |
|------|------|
| `delegate_task` | 生成一个或多个子代理在隔离上下文中并行工作 |

## `file` 工具集

| 工具 | 描述 |
|------|------|
| `patch` | 目标文件查找替换编辑。9 种模糊匹配策略。返回统一 diff |
| `read_file` | 带行号和分页读取文本文件 |
| `search_files` | 搜索文件内容或按名称查找文件。Ripgrep 后端 |
| `write_file` | 写入文件，完全替换现有内容。自动创建父目录 |

## `homeassistant` 工具集

| 工具 | 描述 |
|------|------|
| `ha_call_service` | 调用 Home Assistant 服务控制设备 |
| `ha_get_state` | 获取单个 HA 实体详细状态 |
| `ha_list_entities` | 列出 Home Assistant 实体 |
| `ha_list_services` | 列出可用 HA 服务 |

## `image_gen` 工具集

| 工具 | 描述 | 需求 |
|------|------|------|
| `image_generate` | 使用 FLUX 2 Pro 模型生成高质量图像，自动 2x 放大 | `FAL_KEY` |

## `memory` 工具集

| 工具 | 描述 |
|------|------|
| `memory` | 保存重要信息到持久记忆，跨会话存活。出现在会话启动时的系统提示中 |

## `messaging` 工具集

| 工具 | 描述 |
|------|------|
| `send_message` | 发送到已连接的消息平台，或列出可用目标 |

## `moa` 工具集

| 工具 | 描述 | 需求 |
|------|------|------|
| `mixture_of_agents` | 通过多个前沿 LLM 协作路由难题。5 次 API 调用（4 个参考模型 + 1 个聚合器） | `OPENROUTER_API_KEY` |

## `rl` 工具集

| 工具 | 描述 | 需求 |
|------|------|------|
| `rl_check_status` | 获取训练运行状态和指标。**速率限制**：同一运行检查间隔至少 30 分钟 | `TINKER_API_KEY`, `WANDB_API_KEY` |
| `rl_edit_config` | 更新配置字段 | 同上 |
| `rl_get_current_config` | 获取当前环境配置 | 同上 |
| `rl_get_results` | 获取完成训练运行的最终结果和指标 | 同上 |
| `rl_list_environments` | 列出所有可用 RL 环境 | 同上 |
| `rl_list_runs` | 列出所有训练运行 | 同上 |
| `rl_select_environment` | 选择 RL 环境进行训练 | 同上 |
| `rl_start_training` | 启动新 RL 训练运行 | 同上 |
| `rl_stop_training` | 停止运行中的训练任务 | 同上 |
| `rl_test_inference` | 快速推理测试任何环境 | 同上 |

## `session_search` 工具集

| 工具 | 描述 |
|------|------|
| `session_search` | 搜索过去对话的长期记忆。所有过去会话可搜索，工具总结发生了什么 |

## `skills` 工具集

| 工具 | 描述 |
|------|------|
| `skill_manage` | 管理技能（创建、更新、删除） |
| `skill_view` | 加载技能完整内容或访问链接文件 |
| `skills_list` | 列出可用技能（名称 + 描述） |

## `terminal` 工具集

| 工具 | 描述 |
|------|------|
| `process` | 管理后台进程（list/poll/log/wait/kill/write） |
| `terminal` | 在 Linux 环境执行 shell 命令。设置 `background=true` 启动长时间运行服务器 |

## `todo` 工具集

| 工具 | 描述 |
|------|------|
| `todo` | 管理当前会话任务列表。用于 3+ 步骤复杂任务 |

## `vision` 工具集

| 工具 | 描述 |
|------|------|
| `vision_analyze` | 使用 AI 视觉分析图像 |

## `web` 工具集

| 工具 | 描述 | 需求 |
|------|------|------|
| `web_search` | 搜索网页，返回最多 5 个相关结果 | `EXA_API_KEY` / `PARALLEL_API_KEY` / `FIRECRAWL_API_KEY` / `TAVILY_API_KEY` |
| `web_extract` | 从网页 URL 提取内容，支持 PDF | 同上 |

## `tts` 工具集

| 工具 | 描述 |
|------|------|
| `text_to_speech` | 文本转语音，保存到 `\~/voice-memos/` 或作为语音消息发送 |
