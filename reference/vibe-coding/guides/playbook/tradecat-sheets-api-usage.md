# TradeCat Sheets API 使用 - 配置协议

## 前置条件检查清单

- [ ] Google Sheet 公开链接可访问
- [ ] 具备 `curl` 命令行工具
- [ ] 具备 `python3` 运行环境
- [ ] 具备 JSON 解析能力（Python json 模块）
- [ ] 具备 gzip 解压能力（Python gzip 模块）
- [ ] 网络可访问 Google Sheets API

## 配置步骤（IF-THEN）

### 步骤 1：获取 API 注册表

```
IF 需要发现可用端点
THEN 拉取 API 注册表 CSV
```

```bash
SHEET_ID="1q-2sXGsFYsKf3nV5u5golTVrLH5sfc0doiWwz_kavE4"

# 拉取 API 页 CSV
curl -fsSL "https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:csv&sheet=API&headers=0" > api.csv
```

### 步骤 2：解析端点列表

```
IF 需要列出所有可用端点
THEN 执行端点解析脚本
```

```python
python3 - << 'PY'
import csv, io, json, sys

raw = open("api.csv", "r", encoding="utf-8", errors="replace").read()
rows = list(csv.reader(io.StringIO(raw)))

for r in rows[3:]:  # 跳过 banner/导出信息/表头
    if len(r) < 1 or not r[0].strip().startswith("{"):
        continue
    try:
        obj = json.loads(r[0])
    except Exception:
        continue
    
    sheet = (obj.get("data") or {}).get("sheet") or {}
    title = sheet.get("title")
    gid = sheet.get("gid")
    payload = (obj.get("data") or {}).get("payload") or {}
    schema = payload.get("schema") or payload.get("facts_schema") or ""
    
    if title:
        print(f"- {title} (gid={gid} schema={schema})")
PY
```

### 步骤 3：消费端点数据

```
IF 需要拉取特定端点数据
THEN 复制 API 表中"请求命令"直接执行
```

```bash
# 从 API 表找到目标端点的"请求命令"，通常格式：
curl ... | python3 -c "import ..."
```

## 验证检查点

- [ ] API 注册表 CSV 成功下载（非空文件）
- [ ] 端点解析脚本输出端点列表
- [ ] 返回数据包含 `data.payload` 字段
- [ ] JSON 格式可解析（无语法错误）
- [ ] 响应数据包含 `data.meta.generated_at` 时间戳
- [ ] Schema 与预期匹配（`table_rows_v2` 或 `symbol_query_v2`）

## 数据 Schema 说明

### table_rows_v2

适用于：表格快照类数据（看板/Polymarket/新闻）

```
IF schema 为 table_rows_v2
THEN 以 facts[] 为单一事实来源
```

每条 fact 包含：
- `dims`: 维度信息
- `fields_text`: 文本字段
- `fields_num`: 数值字段

### symbol_query_v2

适用于：单币种多周期指标面板（BTC/ETH/BNB/SOL）

```
IF schema 为 symbol_query_v2
THEN 以 facts[] 为单一事实来源，不要依赖 UI 文案
```

## 端点清单（2026-03-17 快照）

### 市场总览（table_rows_v2）

| 端点 | gid | schema |
|------|-----|--------|
| 加密货币看板 | 1277788455 | table_rows_v2 |
| 宏观大宗看板 | 1931661963 | table_rows_v2 |

### 单币画像（symbol_query_v2）

| 端点 | gid | schema |
|------|-----|--------|
| 币种查询_BTCUSDT | 1325757221 | symbol_query_v2 |
| 币种查询_ETHUSDT | 904473439 | symbol_query_v2 |
| 币种查询_BNBUSDT | 78880380 | symbol_query_v2 |
| 币种查询_SOLUSDT | 208400041 | symbol_query_v2 |

### 预测市场（table_rows_v2）

| 端点 | gid | schema |
|------|-----|--------|
| PolymarketTop15 | 1715937602 | table_rows_v2 |
| Polymarket时段分布 | 333189916 | table_rows_v2 |
| Polymarket类别偏好 | 1923964075 | table_rows_v2 |

### 实时新闻（table_rows_v2）

| 端点 | gid | schema |
|------|-----|--------|
| 实时新闻 | 1419246950 | table_rows_v2 |

## 可靠性建议

| 策略 | 实现 |
|------|------|
| 缓存 | 建议 5～60 秒，按业务容忍度 |
| 重试 | 遇到 429/5xx 时指数退避 |
| 降级 | 表不可用 → 只读旧缓存 |
| 降级 | 新闻不可用 → 只跑行情/指标 |
| 校验 | schema 不匹配 → 拒绝消费 |

## 常见故障

| 问题 | 解决方案 |
|------|----------|
| CSV 下载失败 | 检查网络、验证 SHEET_ID 正确 |
| JSON 解析错误 | 检查 gviz 接口返回格式是否有变化 |
| 数据为空 | 确认端点 gid 正确，检查 API 表更新 |
| 数据过期 | 检查 `data.meta.generated_at` 时间戳 |

## 安全边界

- 本接口不构成投资建议，仅用于研究与协作
- 不在任何公开场合贴出内部密钥（本表为公开资产）
- 不应添加敏感头部到公开日志
