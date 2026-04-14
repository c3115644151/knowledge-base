# Home Assistant 集成

与 Home Assistant 双向集成：实时事件订阅 + 智能家居工具。

## 两种集成方式

1. **Gateway 平台** - 通过 WebSocket 订阅实时状态变化
2. **智能家居工具** - 4 个 LLM 可调用工具

## 配置

### 1. 创建长期访问令牌

1. 打开 Home Assistant
2. 进入 **Profile** → **Long-Lived Access Tokens**
3. 创建令牌（如 "Hermes Agent"）
4. 复制令牌

### 2. 配置环境变量

```bash
# ~/.hermes/.env

# 必需
HASS_TOKEN=your-long-lived-access-token

# 可选
HASS_URL=http://192.168.1.100:8123  # 默认 http://homeassistant.local:8123
```

设置 `HASS_TOKEN` 后，`homeassistant` 工具集自动启用。

### 3. 启动 Gateway

```bash
hermes gateway
```

## 可用工具

### `ha_list_entities`
列出实体，可按 domain 或 area 过滤。
```python
# 参数
domain: "light" | "switch" | "climate" | "sensor" | "binary_sensor" | ...
area: "living room" | "kitchen" | ...
```

### `ha_get_state`
获取单个实体的详细状态。
```python
# 参数
entity_id: "light.living_room" | "climate.thermostat" | ...
```

### `ha_list_services`
列出可用的服务（操作）。
```python
# 参数
domain: "light" | "climate" | ...
```

### `ha_call_service`
调用服务控制设备。
```python
# 参数
domain: "light" | "climate" | "switch" | ...
service: "turn_on" | "turn_off" | "toggle" | "set_temperature" | ...
entity_id: "light.living_room"
data: {"brightness": 128, "color_name": "blue"}  # 可选
```

## Gateway 平台：实时事件

### 配置事件过滤

默认**不转发任何事件**，必须配置：
```yaml
platforms:
  homeassistant:
    enabled: true
    extra:
      watch_domains:
        - climate
        - binary_sensor
        - alarm_control_panel
        - light
      watch_entities:
        - sensor.front_door_battery
      ignore_entities:
        - sensor.uptime
        - sensor.cpu_usage
      cooldown_seconds: 30
```

| 设置 | 默认 | 说明 |
|------|------|------|
| `watch_domains` | 无 | 只监视这些 domain |
| `watch_entities` | 无 | 只监视这些实体 ID |
| `watch_all` | false | 监视所有状态变化 |
| `ignore_entities` | 无 | 始终忽略的实体 |
| `cooldown_seconds` | 30 | 同一实体最小间隔 |

### 事件格式

| Domain | 格式示例 |
|--------|----------|
| `climate` | "HVAC mode changed from 'off' to 'heat' (current: 21, target: 23)" |
| `sensor` | "changed from 21°C to 22°C" |
| `binary_sensor` | "triggered" / "cleared" |
| `alarm_control_panel` | "alarm state changed from 'armed_away' to 'triggered'" |

## 安全

### 被阻止的 Domain
- `shell_command` - 任意 shell 命令
- `command_line` - 执行命令的传感器
- `python_script` - Python 脚本执行
- `pyscript` - 脚本集成
- `hassio` -Addon 控制、关机/重启
- `rest_command` - HTTP 请求（SSRF 向量）

## 示例

### 早间routine
```
用户: Start my morning routine
Agent:
1. ha_call_service(domain="light", service="turn_on", entity_id="light.bedroom", data={"brightness": 128})
2. ha_call_service(domain="climate", service="set_temperature", entity_id="climate.thermostat", data={"temperature": 22})
3. ha_call_service(domain="media_player", service="turn_on", entity_id="media_player.kitchen_speaker")
```

### 安全检查
```
用户: Is the house secure?
Agent:
1. ha_list_entities(domain="binary_sensor")  # 检查门窗传感器
2. ha_get_state(entity_id="alarm_control_panel.home")  # 检查警报状态
3. ha_list_entities(domain="lock")  # 检查锁状态
4. Reports: "All doors closed, alarm is armed_away, all locks engaged."
```
