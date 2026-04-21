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
- "Trying to access unbound value: ResourceKey[minecraft:block / ...]"（NPE 包装）

**NeoForge 26.1 关键行为**： DeferredRegister 的 `register()` 调用**在类加载时就执行工厂函数**，而非延迟到 RegisterEvent。

即：
```java
// 这行代码在类加载时（引用该类时）就执行 factory
public static final DeferredBlock<Block> BLOCK = BLOCKS.register("x", factory);
// 不会等到 RelicRegisters.init(bus) 中的 register(bus) 才执行
```

**常见错误写法**：
```java
// ❌ 错误：在 initBlockEntityType() 中调用 RelicBlocks.BLOCK.get()
// → 触发 RelicBlocks 类加载 → 静态字段初始化 → BLOCKS.register(factory) → factory 执行
// → props.setId(ResourceKey.create(...)) → NPE（block 尚未注册到 registry）
public static void initBlockEntityType() {
    Set<Block> validBlocks = Set.of(RelicBlocks.SUSPICIOUS_MOSSY_STONE_BRICKS.get()); // ← 触发类加载 + 工厂执行
    HOLDER = new BlockEntityType<>(..., validBlocks);
    RelicsBrushableBlock.BLOCK_ENTITY_TYPE = HOLDER;
}
```

**正确模式：不在类加载路径上引用 DeferredBlock**
1. **不在 init() 之前调用 .get()**：任何类加载触发 `.get()` 都会提前执行所有 BLOCKS.register() 工厂
2. **改为延迟到运行时**：BlockEntityType 在 `newBlockEntity()` 首次调用时创建（此时所有 register(bus) 已完成）
3. **不在静态初始化路径上引用对方类**：RelicBlockEntities 不在类加载路径上引用 RelicBlocks

**推荐架构（两选一）**：

方案 A：**延迟初始化 BlockEntityType**
```java
// RelicsBrushableBlock.java
public static BlockEntityType<RelicBrushableBlockEntity> BLOCK_ENTITY_TYPE;

@Override
public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
    if (BLOCK_ENTITY_TYPE == null) {
        // 运行时（首次放置方块时），register(bus) 已完成，安全 .get()
        var block = RelicBlocks.SUSPICIOUS_MOSSY_STONE_BRICKS.get();
        BLOCK_ENTITY_TYPE = new BlockEntityType<>((p, s) -> new RelicBrushableBlockEntity(BLOCK_ENTITY_TYPE, p, s), Set.of(block));
    }
    return new RelicBrushableBlockEntity(BLOCK_ENTITY_TYPE, pos, state);
}

// RelicBlockEntities.java：只注册空的 DeferredHolder（lazy 引用 HOLDER）
static BlockEntityType<RelicBrushableBlockEntity> HOLDER;
public static final DeferredHolder<...> BET = BLOCK_ENTITY_TYPES.register("...", () -> HOLDER);
// HOLDER 由 RelicsBrushableBlock 在运行时设置，DeferredHolder 的 lambda 只在 RegisterEvent 时调用
```

方案 B：**两阶段初始化（先 Block，再 BET）**
```java
// RelicRegisters.init():
// 1. RelicBlocks.getBlocks() 触发类加载 → BLOCKS.register(factory) 入队
// 2. BLOCKS.register(bus) → 执行所有 factory → RelicsBrushableBlock 实例化，BLOCK_ENTITY_TYPE 仍 null
// 3. RelicBlocks.init() → 初始化 BlockItem
// 4. 设置 BLOCK_ENTITY_TYPE = new BlockEntityType<>(..., Set.of(SUSPICIOUS_MOSSY_STONE_BRICKS.get()))
// 5. BET.register(bus) → 填入 HOLDER
```

方案 A 更简洁，推荐使用。

**NeoForge 1.21.11 vs 26.1 对比**：两版本的 `register()` 行为完全相同（类加载时执行工厂），但旧文档中未明确说明此行为，导致错误假设。版本降级不会解决此问题，只需遵循上述正确模式即可。

---

## Entry 1b — BrushableBlock 自定义子类导致 Placement Crash

**根本原因**：Minecraft 的 `BrushableBlock.newBlockEntity()` 方法硬编码创建 vanilla `BrushableBlockEntity`，
其 BlockEntityType 仅关联 vanilla 可疑方块。放置自定义 BrushableBlock 子类时，
`BrushableBlockEntity.validBlocks` 检查失败 → `IllegalStateException: Invalid block entity` crash。

**症状**：放置可疑方块时游戏崩溃：
```
java.lang.IllegalStateException: Invalid block entity minecraft:brushable_block
    at BrushableBlock.newBlockEntity(BrushableBlock.java:...)
```

**修复**：必须创建自定义 `RelicsBrushableBlock extends BrushableBlock` + 自定义 `RelicBrushableBlockEntity`。
在 `newBlockEntity()` 中使用自定义 BlockEntityType（关联自定义方块本身）。

---

## Entry 1c — BlockEntityType 循环依赖（RelicBlockEntities ↔ RelicBlocks）

**根本原因**：RelicBlockEntities 需要 Set<Block> validBlocks，引用 RelicBlocks；
但 RelicBlocks 加载时需要执行 BLOCKS.register(factory)，factory 内创建 RelicsBrushableBlock，
此时如果 RelicBlockEntities.initBlockEntityType() 先执行并调用 `.get()`，会触发双重问题（NPE + 未注册）。

**修复**：不创建预初始化的 BlockEntityType。BlockEntityType 在 `newBlockEntity()` 首次调用时延迟构造：
```java
// RelicsBrushableBlock.newBlockEntity()：
if (BLOCK_ENTITY_TYPE == null) {
    var block = RelicBlocks.SUSPICIOUS_MOSSY_STONE_BRICKS.get(); // 运行时，安全
    BLOCK_ENTITY_TYPE = new BlockEntityType<>(factory, Set.of(block));
}
```

RelicBlockEntities.java 只保留空的 DeferredHolder 注册（HOLDER 后续被赋值），不调用 `.get()`。

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

## M1-M2 阶段卡点记录（2026-04-20）

### Entry 8 — BlockItem 使用 `item.` 前缀的 descriptionId（高优先级）

**根本原因**：`BlockItem.getName()` → `Item.descriptionId` 字段，默认值规则为 `item.<modid>.<name>`。
即使方块的 `descriptionId` 是 `block.relictales.suspicious_mossy_stone_bricks`，
BlockItem 的描述键仍为 `item.relictales.suspicious_mossy_stone_bricks`。

**症状**：方块放置后，创意栏显示 `block.relictales.suspicious_mossy_stone_bricks`（或显示 raw key）。

**错误认知**：
- 以为在 `BlockBehaviour.Properties` 上调用 `overrideDescription()` 可以改变 BlockItem 的显示名
- `descriptionId` 在 `BlockBehaviour` 中是 `private final`，`getDescriptionId()` 是 `final`，无法被子类覆盖

**正确修复**：在语言文件（zh_cn.json / en_us.json）中同时注册 `item.` 前缀的键：
```json
// zh_cn.json
{
  "itemGroup.relictales": "考古物语",
  "block.relictales.suspicious_mossy_stone_bricks": "可疑的苔石砖",
  "item.relictales.suspicious_mossy_stone_bricks": "可疑的苔石砖",
  "item.relictales.jungle_hunter_feather": "丛林猎羽符"
}
```

**无需修改 Java 代码**。Access Transformer 也无法工作（`overrideDescription()` 底层机制不改变 Item 层级）。

---

## Entry 9 — BrushableBlock 自定义 loot 表注入（高优先级）

**根本原因**：使用 `RelicBrushableBlockItem extends BlockItem`，重写 `place()` 放置时将 lootTableId 注入到 BlockEntity。
plain `BlockItem` 无法携带自定义 loot 表数据。

**症状**：刷取完成但不掉落任何物品（lootTable 未设置）。

**关键 API**：
- `RelicBrushableBlockItem` 持有 `private String lootTableId` + `setLootTable(String)` 方法
- `place()` 中从 NBT 读取或使用 `this.lootTableId` 注入 `BlockEntity.setLootTable()`
- `RelicBrushableBlockItem.setLootTable("relictales:blocks/suspicious_mossy_stone_bricks")`

**正确模式**：
```java
// RelicBlocks.init() 中：
SUSPICIOUS_MOSSY_STONE_BRICKS_ITEM = ITEMS.register(
    "suspicious_mossy_stone_bricks",
    id -> {
        var item = new RelicBrushableBlockItem(
            SUSPICIOUS_MOSSY_STONE_BRICKS.get(),
            new Item.Properties().setId(ResourceKey.create(Registries.ITEM, id))
        );
        item.setLootTable("relictales:blocks/suspicious_mossy_stone_bricks");
        return item;
    }
);
```

**相关文件**：
- [RelicBrushableBlockItem.java](src/main/java/com/relictales/content/block/RelicBrushableBlockItem.java)
- [RelicBrushableBlockEntity.java](src/main/java/com/relictales/content/block/RelicBrushableBlockEntity.java) — `spawnLoot()` 方法

---

## Entry 10 — Item 模型引用 `minecraft:` 纹理但本地纹理存在时的紫黑贴图

**根本原因**：item model JSON 中引用了 `minecraft:item/feather` 和 `minecraft:item/suspicious_sand`，
但实际上 `relictales:item/` 目录已存在对应 PNG 文件（16x16 程序化生成的灰阶/绿色贴图）。
引用 `minecraft:` 路径时，游戏找不到正确资源会降级为紫黑缺失纹理。

**症状**：物品在创意栏和世界中显示为紫黑色方块。

**正确修复**：item model JSON 直接引用模组自身纹理（仅在模组已有自定义美术资源时）：
```json
// ✅ 正确：引用模组内置纹理（需确认 relictales:item/ 路径存在）
{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "relictales:item/jungle_hunter_feather"
  }
}
```

**临时方案（无美术资源时）**：引用原版已有纹理，暂用原版资源顶着：
```json
// ✅ 暂用原版羽毛纹理
{
  "parent": "minecraft:item/generated",
  "textures": { "layer0": "minecraft:item/feather" }
}

// ✅ 暂用原版可疑砂砾纹理
{
  "parent": "minecraft:item/generated",
  "textures": { "layer0": "minecraft:item/suspicious_sand" }
}

// ✅ 方块暂用原版可疑砂砾纹理
{
  "parent": "minecraft:block/cube_all",
  "textures": { "all": "minecraft:block/suspicious_gravel" }
}
```

**纹理文件位置**：
- `src/main/resources/assets/relictales/textures/item/jungle_hunter_feather.png`
- `src/main/resources/assets/relictales/textures/block/suspicious_mossy_stone_bricks.png`

---

## 反编译认知修正流程

> 详见 [CLAUDE.md](../CLAUDE.md) 第十四节 — 反编译认知修正流程（强制执行）

**核心原则**：遇到任何无法通过知识库或文档解决的卡点，立即反编译验证，不要猜测。

**反编译命令**：
```bash
./gradlew decompile  # 生成反编译源码到 build/decompiled/
```

**沉淀两步走**：
1. 更新 `NeoForge-开发实践勘误.md`（记录 Entry）
2. 判断是否更新 `CLAUDE.md` 规范表格

---

*沉淀时间：2026-04-21*
*来源项目：RelicTales (RelicTales)*
