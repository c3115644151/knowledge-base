# NeoForge 开发实践勘误

> **来源**：RelicTales 项目开发（2026-04-20）
> **适用版本**：NeoForge 26.1.x / Minecraft 1.21.x
> **目的**：沉淀开发过程中的卡点，纠正错误经验，完善知识库

---

## 经验 1：SoundEvents 考古音效名称（1.21 官方映射）

### 错误认知
根据旧版本（1.20.x）经验，认为音效名为：
- `ITEM_BRUSH_BRUSHING_GENERIC`
- `BRUSH_GENERIC_COMPLETED`

### 正确认知

**1.21 版本命名规范**：Moja ng 官方映射移除了冗余前缀。

| 描述 | 正确字段名（1.21） | 错误字段名（旧） |
|------|------------------|-----------------|
| 刷取中音效 | `SoundEvents.BRUSH_GENERIC` | `ITEM_BRUSH_BRUSHING_GENERIC` |
| 刷取完成音效（砂砾） | `SoundEvents.BRUSH_GRAVEL_COMPLETED` | `BRUSH_GENERIC_COMPLETED` ❌ |
| 刷取完成音效（沙子） | `SoundEvents.BRUSH_SAND_COMPLETED` | 不存在 |

**不存在 `BRUSH_GENERIC_COMPLETED` 或 `BRUSH_COMPLETED`**。

### 正确用法

```java
// ✅ 正确
new BrushableBlock(baseBlock, SoundEvents.BRUSH_GENERIC, SoundEvents.BRUSH_GRAVEL_COMPLETED, props)
```

---

## 经验 2：DeferredRegister.Blocks 注册 BrushableBlock

### 错误认知
使用三参数 `registerBlock(name, factory, properties)` 重载。

### 正确认知

**1.21.10+ 三参数重载已废弃**，必须使用双参数 `register(name, factory)`。

```java
// ✅ 正确（双参数，props 自动注入）
public static final DeferredBlock<BrushableBlock> SUSPICIOUS_BLOCK = BLOCKS.register(
    "suspicious_mossy_stone_bricks",
    props -> new BrushableBlock(
        Blocks.MOSSY_STONE_BRICKS,
        SoundEvents.BRUSH_GENERIC,
        SoundEvents.BRUSH_GRAVEL_COMPLETED,
        props  // NeoForge 自动注入带 ID 的 properties
    )
);

// ❌ 错误（三参数已废弃）
BLOCKS.registerBlock("suspicious_mossy_stone_bricks",
    props -> new BrushableBlock(...),
    BlockBehaviour.Properties.ofFullCopy(Blocks.SUSPICIOUS_SAND)
);
```

---

## 经验 3：StructureProcessor 注册表键

### 错误认知
使用 `Registries.STRUCTURE_PROCESSOR_SERIALIZER`。

### 正确认知

**1.21 中注册表键为 `STRUCTURE_PROCESSOR`**，不是 `STRUCTURE_PROCESSOR_SERIALIZER`。

```java
// ✅ 正确
public static final DeferredRegister<StructureProcessorType<?>> PROCESSORS =
    DeferredRegister.create(Registries.STRUCTURE_PROCESSOR, MOD_ID);

// ❌ 错误（不存在此键）
DeferredRegister.create(Registries.STRUCTURE_PROCESSOR_SERIALIZER, MOD_ID)
```

---

## 经验 4：StructureProcessor.processBlock 方法签名

### 错误认知
使用 `ServerLevelAccessor` 作为第一个参数，参数名为 `blockInfoLocal`。

### 正确认知（1.21 官方 Mojang 映射）

```java
@Nullable
public StructureTemplate.StructureBlockInfo processBlock(
    LevelReader level,                              // ✅ 不是 ServerLevelAccessor
    BlockPos offset,                                // 结构放置基准偏移
    BlockPos pos,                                   // 当前处理方块位置
    StructureTemplate.StructureBlockInfo originalBlockInfo,  // NBT 模板中的原始定义
    StructureTemplate.StructureBlockInfo currentBlockInfo,   // 经前面处理器处理后的当前状态
    StructurePlaceSettings settings
) { ... }
```

**注意**：
- 使用 `originalBlockInfo` 和 `currentBlockInfo` 两个参数区分状态链
- `currentBlockInfo` 是你需要判断和替换的当前状态
- 使用 `level.getRandom()` 获取随机数（`LevelReader` 接口有此方法）

---

## 经验 5：DeferredHolder 泛型参数

### 错误认知
嵌套 `StructureProcessorType<...>` 作为第二个类型参数。

### 正确认知

`DeferredHolder<T, V>` 中 `V` 是最终包装的类型本身，不是嵌套。

```java
// ✅ 正确
public static final DeferredHolder<
    StructureProcessorType<?>,                         // 父类型
    StructureProcessorType<JungleTempleProcessor>       // 自身类型（不嵌套）
> JUNGLE_TEMPLE_PROCESSOR = PROCESSORS.register(...);

// 注册到 DeferredRegister
public static final DeferredHolder<StructureProcessorType<?>, StructureProcessorType<JungleTempleProcessor>> JUNGLE_TEMPLE_PROCESSOR =
    PROCESSORS.register("jungle_temple_processor", () -> () -> MyProcessor.CODEC);
```

---

## 经验 6：丛林神殿是 Legacy 结构（processor_list 不适用）

### 错误认知
认为所有原版遗迹都可以通过 `data/minecraft/worldgen/processor_list/<name>.json` 覆盖注入方块。

### 正确认知

**Minecraft 中存在两种结构**：

| 类型 | 特征 | 可用 processor_list |
|------|------|---------------------|
| **Legacy Feature** | 硬编码 Java 逻辑，无 NBT 模板池 | ❌ 不能 |
| **Jigsaw** | 使用结构池模板，可附加处理器 | ✅ 可以 |

**属于 Legacy 的遗迹**：
- 丛林神殿 `jungle_temple`
- 沙漠神殿 `desert_pyramid`

**属于 Jigsaw 的遗迹**：
- 要塞 `stronghold`
- 下界堡垒 `nether_fortress`
- 末地城 `end_city`
- 村庄（所有变种）
- 废弃矿井 `mineshaft`

### 注入 Legacy 结构的替代方案

**方案 A：BiomeModifier 完全替换**
1. JSON 移除原版结构
2. 自定义 Jigsaw 版结构替代
3. 附加自定义 processor_list

**方案 B：Mixin 拦截（26.1 反混淆后可行）**
```java
@Mixin(JungleTemplePiece.class)
public abstract class MixinJungleTemplePiece {
    @Inject(method = "placeBlock", at = @At("HEAD"), cancellable = true)
    private void onPlaceBlock(WorldGenLevel level, BlockState state, int x, int y, int z,
                               BoundingBox box, CallbackInfoReturnable<Boolean> ci) {
        if (state.is(Blocks.MOSSY_STONE_BRICKS) && level.getRandom().nextFloat() < 0.2f) {
            level.setBlock(new BlockPos(x, y, z),
                ModBlocks.SUSPICIOUS_MOSSY_STONE_BRICKS.get().defaultBlockState(), 3);
            ci.setReturnValue(true);
        }
    }
}
```

---

## 经验 7：Knowledge Base 优先于网络搜索

在本次开发中，遇到每个卡点都通过**知识库 + 搜索**的方式解决。关键原则：

1. **先查知识库**：`knowledge-base/reference/neoForge/` 中已有最新文档
2. **次查官方文档**：`docs.neoforged.net` 有完整的 API 参考
3. **最后搜索**：当以上两者都没有时才用网络搜索
4. **搜索结果要验证**：网络搜索结果（含 AI 摘要）可能包含过时或错误的经验

---

## 相关知识库文档

| 文档 | 修正内容 |
|------|---------|
| `NeoForge-方块.md` | 新增 BrushableBlock 注册章节（含正确语法） |
| `NeoForge-世界生成-结构.md` | 新增 StructureProcessor 章节（含 Legacy 结构说明） |
| `NeoForge-资源-音效.md` | 新增考古音效原版 SoundEvents 名称表 |

---

## M1-M2 阶段卡点记录（2026-04-20）

### Entry 1 — DeferredRegister 时序陷阱（高优先级）

**根本原因**：DeferredRegister.register() 必须在 RegisterEvent 时机执行。
任何在类初始化（<clinit>）时触发的 register() 调用都会失败。

**症状**：
- "Cannot register new entries to DeferredRegister after RegisterEvent has been fired"
- "ExceptionInInitializerError" 包装 IllegalStateException

**常见错误写法**：
```java
// ❌ 错误：static {} 块在类加载时执行，早于 RegisterEvent
static {
    SUSPICIOUS_ITEM = ITEMS.register("item", () -> new Item(...));
}

// ❌ 错误：静态字段初始化器（<> clinit）
public static final DeferredItem<Item> ITEM = ITEMS.register("item", () -> new Item(...));
// 当其他类引用 RelicItems 时会触发类加载，此时 ITEMS 尚未注册到 bus

// ❌ 错误：RelicBlocks 引用 RelicRegisters.ITEMS
// → RelicBlocks 加载 → RelicRegisters.ITEMS 初始化
// → RelicItems 加载（引用 RelicRegisters.ITEMS）
// → 循环依赖，类加载顺序不可控
```

**正确模式：每个注册类持有自己的私有 DeferredRegister**
```java
// RelicBlocks.java
private static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MOD_ID);
// ITEMS.register() 在类加载时执行，但此时只是"入队"，真正注册在 init() 时
public static DeferredItem<BlockItem> MY_ITEM;

public static void init() { // 由 RelicRegisters.init() 调用
    MY_ITEM = ITEMS.register("my_item", id -> new BlockItem(...));
}

public static DeferredRegister.Items getItems() { return ITEMS; }

// RelicRegisters.java
public static void init(IEventBus bus) {
    RelicBlocks.init();      // 触发入队
    RelicBlocks.getItems().register(bus);  // 注册到 bus
}
```

---

### Entry 2 — Item/Block Properties ID 设置（高优先级）

**根本原因**：26.1 中 Item.Properties 和 BlockBehaviour.Properties 必须显式设置资源 ID，
通过 register() 的工厂函数接收 id 参数后调用 setId()。

**症状**：
- "NullPointerException: Block id not set"
- "NullPointerException: Item id not set"

**正确模式（两参数 register 工厂）**：
```java
// Block 注册：props 由 register 内部自动注入（实际传入的是 Identifier）
public static final DeferredBlock<BrushableBlock> BLOCK = BLOCKS.register(
    "my_block",
    id -> {
        BlockBehaviour.Properties props = BlockBehaviour.Properties.ofFullCopy(Blocks.STONE)
            .setId(ResourceKey.create(Registries.BLOCK, id));
        return new BrushableBlock(Blocks.STONE, sound, sound2, props);
    }
);

// Item 注册：同上
public static final DeferredItem<Item> ITEM = ITEMS.register(
    "my_item",
    id -> new Item(new Item.Properties().setId(ResourceKey.create(Registries.ITEM, id)))
);
```

**注意**：register() 工厂的参数是 Identifier，setId() 需要 ResourceKey，因此需要：
- `import net.minecraft.resources.ResourceKey;`
- `import net.minecraft.core.registries.Registries;`
- `setId(ResourceKey.create(Registries.BLOCK, id))` 或 `Registries.ITEM`

---

### Entry 3 — getRandom() 方法位置

**根本原因**：StructureProcessor.processBlock() 的 level 参数是 LevelReader，
没有 getRandom() 方法。RandomSource 应从 StructurePlaceSettings 获取。

**错误**：
```java
LevelReader level = ...
RandomSource random = level.getRandom(); // ❌ LevelReader 没有此方法
```

**正确**：
```java
StructurePlaceSettings settings = ...
RandomSource random = settings.getRandom(blockPos); // ✅
```

---

### Entry 4 — BlockBehaviour 包名

**26.1 中 BlockBehaviour 的正确包名**：
```
net.minecraft.world.level.block.state.BlockBehaviour
```

不是 `net.minecraft.world.level.block.BlockState`，也不是其他变体。

---

*沉淀时间：2026-04-20*
*来源项目：RelicTales (RelicTales)*
