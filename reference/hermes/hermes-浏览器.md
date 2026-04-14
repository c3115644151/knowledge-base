# 浏览器自动化

## 概述

Hermes Agent 支持完整的浏览器自动化，连接多个后端执行网页操作。

## 后端选项

| 后端 | 说明 | 用途 |
|------|------|------|
| `browserbase` | Browserbase 云服务 | 托管浏览器 |
| `browser-use` | Browser Use 云服务 | AI 原生浏览器 |
| `local-chrome` | 本地 Chrome via CDP | 本地开发 |
| `local-chromium` | 本地 Chromium | 开源替代 |

## 配置

```yaml
browser:
  backend: browserbase   # browserbase | browser-use | local-chrome | local-chromium
```

### Browserbase
```yaml
browser:
  backend: browserbase
  browserbase:
    project_id: your-project-id
```

```bash
# ~/.hermes/.env
BROWSERBASE_API_KEY=xxx
BROWSERBASE_PROJECT_ID=xxx
```

### Local Chrome
```yaml
browser:
  backend: local-chrome
  local_chrome:
    debug_port: 9222
```

### Local Chromium
```yaml
browser:
  backend: local-chromium
  local_chromium:
    executable_path: /path/to/chromium
```

## 工具

| 工具 | 说明 | 参数 |
|------|------|------|
| `browser_navigate` | 导航到 URL | `url`, `action` |
| `browser_screenshot` | 截取页面 | `url` (可选) |
| `browser_click` | 点击元素 | `selector` |
| `browser_type` | 输入文本 | `selector`, `text` |
| `browser_scroll` | 滚动页面 | `direction`, `amount` |

## 使用示例

### 基本导航
```
Navigate to https://github.com and show me the trending repositories
```

### 截图
```
Take a screenshot of the current page
```

### 表单填写
```
Go to example.com/login, fill in the username and password, and click submit
```

## Playwright 集成

Browserbase 和 Local Chromium 后端使用 Playwright：

```bash
pip install "hermes-agent[all]"
npx playwright install --with-deps chromium
```

## 资源要求

浏览器自动化需要：
- 至少 2GB 内存
- Playwright 依赖
- Chrome/Chromium 可执行文件

## 安全考虑

1. **网站黑名单** - 可以阻止访问敏感网站
2. **SSRF 防护** - 阻止访问内部网络
3. **容器隔离** - 建议使用 Docker 后端
