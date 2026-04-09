# NeoForge 游戏测试框架

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/misc/gametest

## 概述

游戏测试（Game Tests）是 Minecraft 内置的单元测试框架，用于在游戏中运行自动化测试，验证模组的正确性。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `GameTestHelper` | 游戏测试辅助类 |
| `GameTestInfo` | 测试信息 |
| `TestData` | 测试数据 |
| `TestInstance` | 测试实例 |

---

## 代码示例

### 创建测试结构

```
# 使用 /test pos 获取坐标
# 结构保存在 data/<namespace>/structure/<name>.nbt
```

### 创建测试环境

```json
// data/examplemod/test_environment/default.json
{
    "type": "minecraft:game_rules",
    "rules": {
        "minecraft:fire_damage": false
    }
}
```

### 创建测试实例

```json
// data/examplemod/test_instance/example_test.json
{
    "environment": "examplemod:default",
    "structure": "examplemod:example_structure",
    "max_ticks": 400,
    "setup_ticks": 0,
    "required": true,
    "rotation": "none",
    "type": "minecraft:function",
    "function": "examplemod:example_test"
}
```

### 创建测试函数

```java
// 注册测试函数
public static final DeferredRegister<Consumer<GameTestHelper>> 
    TEST_FUNCTIONS = 
    DeferredRegister.create(
        BuiltInRegistries.TEST_FUNCTION, MOD_ID);

public static final DeferredHolder<Consumer<GameTestHelper>, 
        Consumer<GameTestHelper>> EXAMPLE_TEST = 
    TEST_FUNCTIONS.register("example_test", () -> helper -> {
        // 测试逻辑
        BlockPos pos = helper.absolutePos(new BlockPos(0, 1, 0));
        
        // 断言方块存在
        helper.assertBlockPresent(
            Blocks.DIAMOND_BLOCK, pos);
        
        // 标记成功
        helper.succeed();
    });
```

### 运行测试

```
# 使用命令运行测试
/test runall      # 运行所有测试
/test run <name>  # 运行指定测试
/test runclosest  # 运行最近的测试
```

---

## 注意事项

### 测试隔离
- 每个测试独立运行
- 使用结构模板确保环境一致
- 合理设置 `setup_ticks`

### 常见错误
1. **测试超时**：`max_ticks` 设置过小
2. **条件不满足**：确保前置条件正确
3. **并发问题**：测试间应互相独立

---

## 关联引用

- 模组开发：[NeoForge-入门](./NeoForge-入门.md)
