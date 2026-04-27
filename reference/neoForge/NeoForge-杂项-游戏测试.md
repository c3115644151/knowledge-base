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

## BrushableBlockEntity 测试

### 测试框架选择

使用 `DeferredRegister<Consumer<GameTestHelper>>` + `FunctionGameTestInstance` 程序化注册模式（无需 NBT 结构文件）。

### 注册模式（三步）

**Step 1** — 在测试类中定义测试函数和注册器：
```java
public class MyTest {
    private static final DeferredRegister<Consumer<GameTestHelper>> TEST_FUNCTIONS =
        DeferredRegister.create(Registries.TEST_FUNCTION, MOD_ID);

    private static DeferredHolder<Consumer<GameTestHelper>, Consumer<GameTestHelper>> TEST1;

    static {
        TEST1 = TEST_FUNCTIONS.register("test_name", () -> helper -> {
            // 测试逻辑
        });
    }

    public static void register(IEventBus bus) {
        TEST_FUNCTIONS.register(bus);
        bus.addListener(RegisterGameTestsEvent.class, MyTest::onRegisterGameTests);
    }
}
```

**Step 2** — 在 `RegisterGameTestsEvent` 中注册实例：
```java
private static void onRegisterGameTests(RegisterGameTestsEvent event) {
    Holder<TestEnvironmentDefinition<?>> defaultEnv = event.registerEnvironment(
        Identifier.fromNamespaceAndPath(MOD_ID, "default"),
        new TestEnvironmentDefinition.AllOf()
    );

    TestData<Holder<TestEnvironmentDefinition<?>>> testData = new TestData<>(
        defaultEnv,
        Identifier.fromNamespaceAndPath("minecraft", "empty"),
        100,    // maxTicks
        5,      // setupTicks
        true    // required
    );

    FunctionGameTestInstance instance = new FunctionGameTestInstance(TEST1.getKey(), testData);
    event.registerTest(Identifier.fromNamespaceAndPath(MOD_ID, "test_name"), instance);
}
```

**Step 3** — 在主类中注册：
```java
// RelicTales.java 构造函数
MyTest.register(bus);
```

### 刷取测试核心模式

```java
TEST = TEST_FUNCTIONS.register("brushing_test", () -> helper -> {
    BlockPos pos = new BlockPos(0, 2, 0);
    helper.setBlock(pos, ModBlocks.CUSTOM_SUSPICIOUS_BLOCK.get());

    helper.runAfterDelay(5, () -> {
        BrushableBlockEntity be = helper.getBlockEntity(pos, BrushableBlockEntity.class);
        BrushableBlockEntityAccessor acc = (BrushableBlockEntityAccessor) be;

        // 设置战利品表和刷取状态
        acc.setLootTable(TEST_LOOT_KEY);
        acc.setBrushCount(100);         // > REQUIRED_BRUSHES_TO_BREAK (10)

        ServerLevel level = (ServerLevel) helper.getLevel();
        LivingEntity brusher = (LivingEntity) helper.spawn(EntityType.COW, pos.above());
        be.brush(level.getGameTime(), level, brusher, Direction.UP, new ItemStack(Items.BRUSH));

        // 1. 方块替换检查（立即，brush() 调用时同步完成）
        if (!helper.getBlockState(pos).is(Blocks.BASE_BLOCK)) { helper.fail("Not converted!"); return; }

        // 2. 掉落物检测（需延迟 1 tick — addFreshEntity 待处理队列）
        BlockPos worldPos = be.getBlockPos();
        helper.runAfterDelay(1, () -> {
            var items = level.getEntitiesOfClass(
                ItemEntity.class, new AABB(worldPos).inflate(3.0));
            if (items.isEmpty()) { helper.fail("No loot!"); return; }
            helper.succeed();
        });
    });
});
```

## 陷阱与注意事项

### 1. 绝对坐标 vs 相对坐标

`GameTestHelper` 的便捷方法使用相对坐标（相对于测试结构原点），但 `level.getEntitiesOfClass(AABB)` 使用**绝对世界坐标**。

```java
// ❌ 错误：pos 是相对坐标
BlockPos pos = new BlockPos(0, 2, 0);
level.getEntitiesOfClass(ItemEntity.class, new AABB(pos).inflate(3.0));

// ✅ 正确：从 BlockEntity 获取绝对坐标
BlockPos worldPos = be.getBlockPos();
level.getEntitiesOfClass(ItemEntity.class, new AABB(worldPos).inflate(3.0));

// ✅ 正确：使用 helper 转换
BlockPos absolutePos = helper.absolutePos(new BlockPos(0, 2, 0));
```

### 2. `addFreshEntity()` 待处理队列延迟

`ServerLevel.addFreshEntity()` 将实体放入**待处理队列**，同一 tick 结束时才实际添加。检测掉落物必须延迟到下一 tick：

```java
be.brush(...);
// ❌ 此时实体还在 pending queue
level.getEntitiesOfClass(...)  // 找不到

// ✅ 延迟 1 tick
helper.runAfterDelay(1, () -> {
    level.getEntitiesOfClass(...)  // 能找到
});
```

### 3. Vanilla REQUIRED_BRUSHES_TO_BREAK = 10

`BrushableBlockEntity.REQUIRED_BRUSHES_TO_BREAK` 在 MC 26.1 中为 **10**（不是 100）。测试中设置 `brushCount = 100` 确保单次 `brush()` 即触发完成。

### 4. 测试隔离

- 每个测试独立运行，使用 `minecraft:empty` 结构
- 设置足够的 `maxTicks`（刷取测试建议 120+）
- `setupTicks`（如 5）确保 BlockEntity 完全初始化

### 5. Vanilla 回归测试

确保自定义 BlockEntity 不干扰原版方块：
```java
helper.setBlock(pos, Blocks.SUSPICIOUS_GRAVEL);
// 验证 BE 类型是 vanilla BrushableBlockEntity，不是自定义子类
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
