# NeoForge 更新检查器

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/misc/updatechecker

## 概述

NeoForge 提供了轻量级的更新检查框架，允许模组检查并向玩家显示可用更新。

## 配置

### mods.toml 配置

```toml
[[mods]]
modId = "examplemod"
version = "${version}"
displayName = "Example Mod"

# 添加更新 JSON URL
updateJSONURL = "https://example.com/update.json"
```

### update.json 格式

```json
{
    "homepage": "https://example.com",
    "1.21.11": {
        "1.0.0": "Initial release",
        "1.0.1": "Bug fixes"
    },
    "promos": {
        "1.21.11-recommended": "1.0.1",
        "1.21.11-latest": "1.0.1"
    }
}
```

---

## 代码示例

### 检查更新结果

```java
// 获取更新状态
public static void checkForUpdates(ModInfo modInfo) {
    VersionChecker.Result result = 
        VersionChecker.getResult(modInfo);
    
    if (result != null) {
        VersionChecker.Status status = result.status();
        
        switch (status) {
            case UP_TO_DATE -> {
                // 已是最新版本
            }
            case OUTDATED -> {
                // 有可用更新
                String targetVersion = result.target().version();
            }
            case BETA_OUTDATED -> {
                // 有测试版更新
            }
            case FAILED -> {
                // 检查失败
            }
        }
    }
}

// 获取特定模组的更新
public static void checkMod(String modId) {
    ModContainer container = ModList.get()
        .getModContainerById(modId)
        .orElse(null);
    
    if (container != null) {
        VersionChecker.Result result = 
            VersionChecker.getResult(container.getModInfo());
        // 处理结果
    }
}
```

---

## 注意事项

### 版本格式
- 建议使用语义化版本
- `ComparableVersion` 类支持常见版本格式

### 常见错误
1. **URL 不可达**：检查 JSON URL 是否正确
2. **版本解析失败**：使用标准版本格式
3. **检查延迟**：更新检查可能需要时间

---

## 关联引用

- 配置系统：[相关文档]
