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

## Entry 10 — Item 模型贴图引用与 `items/` ClientItem 双层结构（高优先级）

**根本原因**：Minecraft 1.21.x 的物品模型系统由两层组成：
1. **`models/item/`** — ItemModel JSON（定义几何形状 + 纹理引用）
2. **`items/`** — ClientItem JSON（渲染配置，引用上面的 ItemModel）

仅有 `models/item/` JSON 不足以让游戏找到模型。必须同时创建 `items/` 下的 ClientItem 文件。

**症状**：
- 物品在创意栏和世界中显示为紫黑色方块
- 日志警告：`Missing item model for location relictales:xxx`

**错误认知**：
- 认为 `models/item/<name>.json` 能被游戏自动加载
- 以为 `BlockItem` 的物品模型由 `models/item/` 唯一决定

**正确认知**：1.21.x 的 `BlockItem.getItemModel()` 使用 `ITEM_MODEL` 数据组件（默认值为物品资源 ID），由 `ClientItemInfoLoader` 从 `items/` 目录加载 ClientItem 配置。ClientItem 配置通过 `type: "minecraft:model"` 引用 `models/item/` 下的 ItemModel。

**正确修复**：

步骤 1 — 在 `models/item/` 创建 ItemModel JSON：
```json
// assets/relictales/models/item/jungle_hunter_feather.json
{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "relictales:item/jungle_hunter_feather"
  }
}
```

步骤 2 — 在 `items/` 创建 ClientItem JSON（引用 ItemModel）：
```json
// assets/relictales/items/jungle_hunter_feather.json
{
  "model": {
    "type": "minecraft:model",
    "model": "relictales:item/jungle_hunter_feather"
  }
}
```

**Vanilla 参考**：所有原版可疑方块都有 `items/` 下的 ClientItem 文件：
- `assets/minecraft/items/suspicious_sand.json`
- `assets/minecraft/items/suspicious_gravel.json`
- `assets/minecraft/items/suspicious_red_sand.json`

**官方文档**：
- `models/item/` — docs.neoforged.net/docs/resources/client/models/
- `items/` — docs.neoforged.net/docs/resources/client/models/items
---

## Entry 11 — Mixin config 路径解析（Windows path separator bug）

**根本原因**：NeoForge ModDevGradle 的 `InDevFolderLocator` 使用 `JarContents.ofPaths()` 创建 `CompositeJarContents`。
在 Windows 上，`Path.resolve(String)` 不转换正斜杠（`/`），导致 `META-INF/relictales.mixins.json` 被解析为无效路径。

**症状**：
```
net.neoforged.fml.ModLoadingException: Loading errors encountered:
  - A mixin config named relictales.mixins.json was declared in C:/.../build/classes/java/main, but doesn't exist
```

**错误认知**：
- 认为 `neoforge.mods.toml` 中 `[[mixins]] config="relictales.mixins.json"` 引用 `META-INF/relictales.mixins.json`
- 认为 Mixin JSON 必须放在 `META-INF/` 子目录

**正确认知**：
1. NeoForge 从 **classes 目录的根**读取 mixin JSON（`FolderJarContents` 机制）
2. Mixin JSON 必须放在 source set 的**根目录**，而不是 `META-INF/` 子目录
3. `neoforge.mods.toml` 中 `config="${mod_id}.mixins.json"` 直接引用文件名（如 `relictales.mixins.json`），从 classes 根目录解析

**正确文件结构**：
```
src/main/resources/
├── relictales.mixins.json        ← ✅ 根目录
└── META-INF/
    └── neoforge.mods.toml        ← Mixin config 不在这里
```

**build.gradle 配置**：
```groovy
tasks.register('copyMixinConfigToClasses', Copy) {
    from 'src/main/resources'
    into "${sourceSets.main.output.classesDirs.first()}"  // 复制到 classes 根目录
    include '*.mixins.json'
}
compileJava.dependsOn copyMixinConfigToClasses

afterEvaluate {
    tasks.named('runClient') { it.dependsOn copyMixinConfigToClasses }
    tasks.named('jar') { it.dependsOn copyMixinConfigToClasses }
}

// 处理 JAR 重复条目（META-INF 可能同时出现在 classes 和 resources）
tasks.named('jar') {
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
}
```

**neoforge.mods.toml**：
```toml
[[mixins]]
config="${mod_id}.mixins.json"  # 从 classes 根目录解析，不是 META-INF/
```

---

## Entry 12 — Mixin `Unable to locate obfuscation mapping` 与 `remap = false`

**根本原因**：NeoForge dev 环境（MCP 名称）与生产环境（SRG 名称）的映射脱节。
Mixin 注解处理器期望 SRG→MCP 映射文件，但 ModDevGradle 环境下这些映射文件可能缺失或版本不匹配。

**症状**：
```
Unable to locate obfuscation mapping for @Inject target postProcess
Critical injection failure: @Inject annotation on relictales$replaceMossyBricks could not find any targets matching 'placeBlock'
```

**错误认知**：
- 认为 `remap = true`（默认）是正确的，应该让 Mixin 自动处理映射
- 认为方法名 `postProcess` 在 dev 环境和生产环境都是有效的

**正确修复**：在 `@Mixin` 和 `@Inject` 上同时添加 `remap = false`：
```java
@Mixin(value = JungleTemplePiece.class, remap = false)
public abstract class MixinJungleTemplePiece {

    @Inject(method = "postProcess", at = @At("TAIL"), remap = false)
    private void relictales$replaceMossyBricks(..., CallbackInfo ci) {
        // 直接使用 MCP 名称（dev 环境已反混淆）
    }
}
```

**注意**：
- `remap = false` 意味着 Mixin 不会重新映射方法名/字段名
- 仅在 dev 环境（MCP 已反混淆）使用，生产环境（SRG）需要另外处理
- 对于 ModDevGradle 开发环境，`remap = false` 是正确选择

**Mixing 配置也要确保正确**：
```json
{
  "required": true,
  "package": "com.relictales.mixin",
  "compatibilityLevel": "JAVA_21",
  "mixins": ["MixinJungleTemplePiece"],
  "injectors": { "defaultRequire": 1 }
}
```

---

## Entry 13 — JungleTemplePiece 的 `placeBlock` 方法解析

**根本原因**：`JungleTemplePiece` 本身不定义 `placeBlock` 方法，该方法继承自父类 `StructurePiece`。
因此 `@Inject(method = "placeBlock", ...)` 无法匹配任何 target。

**症状**：
```
Critical injection failure: could not find any targets matching 'placeBlock' in JungleTemplePiece
```

**正确认知**：
- `JungleTemplePiece extends ScatteredFeaturePiece extends StructurePiece`
- `placeBlock()` 在 `StructurePiece` 中定义，`JungleTemplePiece` 未 override
- Mixin 只能注入**当前类直接定义或继承的方法**，不能注入父类方法（需要 mixin 父类）

**正确注入方法**：使用 `@Inject(method = "postProcess", at = @At("TAIL"))` 拦截 `postProcess`（在结构生成完毕后扫描替换方块）：

```java
@Mixin(value = JungleTemplePiece.class, remap = false)
public abstract class MixinJungleTemplePiece {

    @Inject(method = "postProcess", at = @At("TAIL"), remap = false)
    private void relictales$replaceMossyBricks(
            WorldGenLevel level,
            StructureManager structureManager,
            ChunkGenerator chunkGenerator,
            RandomSource random,
            BoundingBox boundingBox,
            ChunkPos chunkPos,
            BlockPos referencePos,
            CallbackInfo ci
    ) {
        // 后置扫描：postProcess 完成后，遍历 BoundingBox 内的 MOSSY_STONE_BRICKS
        BlockPos.MutableBlockPos mutablePos = new BlockPos.MutableBlockPos();
        for (int x = boundingBox.minX(); x <= boundingBox.maxX(); x++) {
            for (int y = boundingBox.minY(); y <= boundingBox.maxY(); y++) {
                for (int z = boundingBox.minZ(); z <= boundingBox.maxZ(); z++) {
                    mutablePos.set(x, y, z);
                    if (level.getBlockState(mutablePos).is(Blocks.MOSSY_STONE_BRICKS)) {
                        level.setBlock(mutablePos,
                            RelicBlocks.SUSPICIOUS_MOSSY_STONE_BRICKS.get().defaultBlockState(), 3);
                    }
                }
            }
        }
    }
}
```

**`postProcess` 方法签名（MCP 反编译源码）**：
```java
public void postProcess(
    WorldGenLevel level,
    StructureManager structureManager,
    ChunkGenerator generator,
    RandomSource random,
    BoundingBox chunkBB,
    ChunkPos chunkPos,
    BlockPos referencePos  // ← 注意最后一个参数是 BlockPos，不是 BoundingBox
)
```

---

---
## Entry 14 — MC 26.1 战利品表目录路径变更：`loot_tables/` → `loot_table/`（高优先级）

**根本原因**：Minecraft 26.1 将数据包中的战利品表目录从复数 `loot_tables/` 改为单数 `loot_table/`。这是一个 DLC（Data Loading Change）层面的破坏性变更，与 Java API 无关。

**症状**：考古可疑方块刷取完成后不产生任何掉落物。日志无错误，`setLootTable()` 成功设置 ResourceKey，但 `dropContent()` 找不到战利品表，返回空物品。

**错误认知**：
- 认为目录名仍然是 `data/<namespace>/loot_tables/`（1.21.11 的路径）
- 查找 MC 26.1 变更文档时忽略了 DLC（Data Loading Change）层面的目录变更

**正确认知**：

| 版本 | 战利品表目录 | 其他数据包目录变化 |
|------|-------------|-------------------|
| 1.21.11 | `data/<ns>/loot_tables/`（复数） | `advancements/`, `recipes/` 等 |
| 26.1 | **`data/<ns>/loot_table/`**（单数） | `advancement/`, `recipe/` 等也改为单数 |

**验证方法**：
1. 反编译 `LootTable` 相关加载代码确认路径
2. 查看原版资源包路径：`assets/minecraft/loot_table/`（空目录存在）
3. 检查 `BuiltInRegistries.LOOT_TABLE` 注册表是否包含自定义资源键

**正确文件位置**：
```
# ✅ 26.1 正确路径
src/main/resources/data/relictales/loot_table/blocks/suspicious_mossy_cobblestone.json

# ❌ 1.21.11 旧路径（26.1 不加载）
src/main/resources/data/relictales/loot_tables/blocks/suspicious_mossy_cobblestone.json
```

**迁移注意**：不仅是 `loot_table/`，其它数据包目录也在 26.1 中改为单数形式。检查 `NeoForge-迁移-1.21.11到26.1.md` 第 7 节 Pack Changes。

---

## Entry 15 — 考古战利品表格式（Archaeology Loot Table）独立于方块战利品表（高优先级）

**根本原因**：考古使用的 `BrushableBlockEntity` 在 `unpackLootTable()` 中通过 `LootContextParamSets.ARCHAEOLOGY` 参数集加载战利品表。方块类型的战利品表（`type: minecraft:block`）使用 `LootContextParamSets.BLOCK` 参数集，两者完全独立。

**症状**：设置了 lootTable ResourceKey 但仍无法掉落物品。战利品表 JSON 使用 `"type": "minecraft:block"` 格式，但考古系统期望的是 `"type": "minecraft:archaeology"` 格式。

**错误认知**：
- 认为考古可疑方块使用普通的方块掉落表（`type: minecraft:block`）
- 把考古战利品表格式与普通方块/实体战利品表混为一谈
- 认为 pool 中的 conditions（如 `survives_explosion`）对考古类型有效

**正确认知**：

### 考古战利品表的特殊要求

| 属性 | 方块战利品表 | 考古战利品表 |
|------|-------------|-------------|
| `type` | `minecraft:block` | **`minecraft:archaeology`** |
| 上下文参数集 | `LootContextParamSets.BLOCK` | `LootContextParamSets.ARCHAEOLOGY` |
| `rolls` 类型 | int 或 `NumberProvider` | **float**（如 `1.0`、`{ "min": 1.0, "max": 3.0 }`）|
| pool conditions | 支持 | **不支持**（`LootContextParamSets.ARCHAEOLOGY` 无上下文参数）|
| `random_sequence` | 可选 | **建议显式设置** |
| `bonus_rolls` | 支持 | 通常为 `0.0` |

### 正确格式

```json
{
  "type": "minecraft:archaeology",
  "pools": [
    {
      "rolls": 1.0,
      "bonus_rolls": 0.0,
      "entries": [
        { "type": "minecraft:item", "name": "relictales:jungle_hunter_feather", "weight": 1 },
        { "type": "minecraft:item", "name": "minecraft:bone", "weight": 2 },
        { "type": "minecraft:item", "name": "minecraft:emerald", "weight": 1 }
      ]
    }
  ],
  "random_sequence": "relictales:blocks/suspicious_mossy_cobblestone"
}
```

### 关键区别（vs 方块战利品表）
1. `rolls` 使用 **float** 而非 int/int provider（`1.0` 而非 `1`）
2. **不能**有 pool level conditions（如 `survives_explosion`），因为 ARCHAEOLOGY 参数集没有 `DamageSource` 等上下文
3. 使用 `entries[].weight` 权重系统（而非 `entries[].functions`）
4. `type` 必须为 `minecraft:archaeology`

### 反编译证据

- `BrushableBlockEntity.unpackLootTable()` L194-203：调用 `this.level.getServer().reloadableRegistries().getLootTable(this.lootTable)`，然后 `lootTable.getRandomItems(paramsBuilder.create(LootContextParamSets.ARCHAEOLOGY))`
- `LootContextParamSets.ARCHAEOLOGY`：定义在 `LootContextParamSets` 中，参数集为 `EMPTY`（无参数）

---

## Entry 16 — BrushableBlockEntity 内部生命周期与刷取流程（核心溯源）

**根本原因**：在调试刷取不掉物的问题时，必须理解 `BrushableBlockEntity` 的内部状态机流转。通过 javap 反编译字节码核验了完整生命周期。

**相关类**：`net.minecraft.world.level.block.entity.BrushableBlockEntity`

### 核心状态字段

| 字段 | 类型 | 作用 |
|------|------|------|
| `lootTable` | `ResourceKey<LootTable>` | 战利品表引用（可为 null） |
| `lootTableSeed` | `long` | 随机种子 |
| `brushCount` | `int` | 已刷次数，达到 `REQUIRED_BRUSHES_TO_BREAK` 即完成 |
| `item` | `ItemStack` | 当前刷取进度显示的物品（客户端渲染） |
| `hitDirection` | `Direction` | 刷取方向（影响粒子效果） |

### 刷取方法签名（26.1）

```java
public void brush(long tick, ServerLevel level, LivingEntity entity, Direction hitDir, ItemStack brushStack) {
    // 1. unpackLootTable() 首次调用 — 从 lootTable 生成 this.item
    // 2. brushCount++
    // 3. 检查 brushCount >= REQUIRED_BRUSHES_TO_BREAK (=10)
    //     → brushingCompleted(level, entity, brushStack)
    //     → 内部调用 dropContent(level, entity, brushStack)
    // 4. checkReset() — 长期不刷则重置
}
```

### 完整调用链

```
brush(long, ServerLevel, LivingEntity, Direction, ItemStack)
  ├─ unpackLootTable(ServerLevel, LivingEntity, ItemStack)
  │    └─ level.getServer().reloadableRegistries().getLootTable(this.lootTable)
  │         └─ 如果 lootTable == null → 跳过，使用已有的 this.item
  │    └─ lootTable.getRandomItems(paramsBuilder.create(ARCHAEOLOGY))
  │    └─ 将结果写入 this.item
  │
  ├─ brushCount++  ← 在 unpackLootTable 之后递增
  │
  ├─ if (brushCount >= REQUIRED_BRUSHES_TO_BREAK)  // REQUIRED_BRUSHES_TO_BREAK = 10
  │    └─ brushingCompleted(ServerLevel, LivingEntity, ItemStack)
  │         └─ dropContent(ServerLevel, LivingEntity, ItemStack)
  │              ├─ unpackLootTable(level, entity, brushStack)  // 再次调用，检查 lootTable 是否 null
  │              │    └─ 如果 lootTable != null: 读取战利品表，更新 this.item
  │              │    └─ 如果 lootTable == null: skip，保持已有 this.item
  │              ├─ if (this.item.isEmpty()) → skip
  │              ├─ ItemEntity itemEntity = new ItemEntity(...)
  │              ├─ level.addFreshEntity(itemEntity)  ← 将实体加入待处理队列
  │              ├─ ItemStack.split(int) → 减少 count
  │              └─ this.item = ItemStack.EMPTY  ← 清空进度物品
  │
  └─ checkReset() — 如果 brushCount 长时间未增加，重置回初始状态
```

### 关键常量

```java
public static final int REQUIRED_BRUSHES_TO_BREAK = 10;  // 刷取完成需要的次数
```

### 刷取进度更新的时序

每次调用 `brush()` 时发生的更新（按顺序）：
1. 首次调用 `unpackLootTable()` — 读取战利品表，设置 `this.item`（客户端可见进度物品）
2. `brushCount++`
3. 达到 `REQUIRED_BRUSHES_TO_BREAK` → 掉落物品
4. 每次 `brush()` 调用后，`LevelRenderer` 会收到更新并渲染 `this.item` 的显示

### 调试验证关键

- `brushCount` 从 0 开始，到 `>= REQUIRED_BRUSHES_TO_BREAK(10)` 触发完成
- 测试中可以使用 `Accessor` 快速设置 `brushCount=100` 以绕过等待
- `addFreshEntity()` 将物品放入**待处理队列**，同一 tick 的实体查询**不会找到**
- `REQUIRED_BRUSHES_TO_BREAK` 是**硬编码 10**，不是可配置值

---

## Entry 17 — 游戏测试（GameTest Framework）中实体检测陷阱

**根本原因**：游戏测试框架的 GameTestHelper 提供便捷方法如 `setBlock()`、`getBlockEntity()` 处理相对坐标，但其他 API（如 `level.getEntitiesOfClass()`）使用绝对世界坐标。错误混用会导致检测不到实体。

**涉及文件**：`src/main/java/com/relictales/test/RelicBrushInteractionTest.java`

### 陷阱 1：绝对坐标 vs 相对坐标

**GameTestHelper 的方法**：
| 方法 | 坐标类型 | 说明 |
|------|---------|------|
| `helper.setBlock(pos)` | 相对 | `(0, 2, 0)` = 相对于测试结构原点 |
| `helper.getBlockEntity(pos)` | 相对 | 同上 |
| `helper.getBlockState(pos)` | 相对 | 同上 |
| `helper.spawn(entity, pos)` | 相对 | 同上 |
| `level.getEntitiesOfClass(AABB)` | **绝对** | 使用世界绝对坐标 |

**错误写法**：
```java
// ❌ pos 是相对坐标 (0, 2, 0)，但 getEntitiesOfClass 需要绝对坐标
BlockPos pos = new BlockPos(0, 2, 0);
var items = level.getEntitiesOfClass(ItemEntity.class, new AABB(pos).inflate(3.0));
```

**正确写法**：
```java
// ✅ 从 BlockEntity 获取绝对坐标
BlockPos worldPos = be.getBlockPos();  // 绝对坐标（由 GameTestHelper 设置）
var items = level.getEntitiesOfClass(ItemEntity.class, new AABB(worldPos).inflate(3.0));
```

**或使用 helper 的绝对坐标转换**：
```java
BlockPos absolutePos = helper.absolutePos(new BlockPos(0, 2, 0));
```

### 陷阱 2：`addFreshEntity()` 待处理队列延迟

**根本原因**：`ServerLevel.addFreshEntity()` 不立即将实体添加到实体列表。实体被放入**待处理队列**（pending queue），在同一 tick 结束时才实际添加。因此，`brush()` 调用**同一 tick** 无法找到掉落物实体。

**错误写法**：
```java
be.brush(tick, level, brusher, Direction.UP, brushStack);
// ❌ 实体还在 pending queue，找不到
var items = level.getEntitiesOfClass(ItemEntity.class, ...);
if (items.isEmpty()) helper.fail("No loot!");
```

**正确写法**（延迟 1 tick）：
```java
be.brush(tick, level, brusher, Direction.UP, brushStack);

// 写操作在同一 tick，读操作延迟到下一 tick
helper.runAfterDelay(1, () -> {
    var items = level.getEntitiesOfClass(ItemEntity.class, new AABB(worldPos).inflate(3.0));
    if (items.isEmpty()) helper.fail("No loot!");
    else helper.succeed();
});
```

### 陷阱 3：Vanilla REQUIRED_BRUSHES_TO_BREAK = 10（非 100）

**重要**：`BrushableBlockEntity.REQUIRED_BRUSHES_TO_BREAK` 在 Minecraft 26.1 中为 **10**。设置 `brushCount = 100` 可确保一次 `brush()` 调用即触发完成。不需要设置 `REQUIRED_BRUSHES_TO_BREAK` 本身（它是 `static final`）。

### 正确测试模式

```java
// ✅ 完整刷取测试模式
helper.setBlock(pos, ModBlocks.CUSTOM_SUSPICIOUS_BLOCK.get());
helper.runAfterDelay(5, () -> {
    BrushableBlockEntity be = helper.getBlockEntity(pos, BrushableBlockEntity.class);
    BrushableBlockEntityAccessor acc = (BrushableBlockEntityAccessor) be;

    // 设置战利品表和刷取状态
    acc.setLootTable(TEST_LOOT_KEY);
    acc.setBrushCount(100);         // > REQUIRED_BRUSHES_TO_BREAK (10)
    acc.setHitDirection(Direction.UP);

    ServerLevel level = (ServerLevel) helper.getLevel();
    LivingEntity brusher = (LivingEntity) helper.spawn(EntityType.COW, pos.above());
    be.brush(level.getGameTime(), level, brusher, Direction.UP, new ItemStack(Items.BRUSH));

    // 1. 方块替换检查（立即）
    if (!helper.getBlockState(pos).is(Blocks.BASE_BLOCK)) { helper.fail("Block not converted!"); return; }

    // 2. 物品检测（延迟 1 tick）
    BlockPos worldPos = be.getBlockPos();
    helper.runAfterDelay(1, () -> {
        var items = level.getEntitiesOfClass(ItemEntity.class, new AABB(worldPos).inflate(3.0));
        if (items.isEmpty()) { helper.fail("No loot!"); return; }
        helper.succeed();
    });
});
```

---

## Entry 18 — `FunctionGameTestInstance` 程序化注册模式（M2 新增）

**根本原因**：NeoForge 26.1 游戏测试框架需要显式的程序化注册。仅通过 `DeferredRegister<Consumer<GameTestHelper>>` 注册 lambda 不足，还需在 `RegisterGameTestsEvent` 中创建 `FunctionGameTestInstance`。

### 正确注册模式（三步）

**Step 1 — 定义测试函数**：
```java
public static final DeferredRegister<Consumer<GameTestHelper>> TEST_FUNCTIONS =
    DeferredRegister.create(Registries.TEST_FUNCTION, RelicTales.MOD_ID);

private static DeferredHolder<Consumer<GameTestHelper>, Consumer<GameTestHelper>> TEST1;

static {
    TEST1 = TEST_FUNCTIONS.register("test_name", () -> helper -> {
        // 测试逻辑
    });
}
```

**Step 2 — 注册到 EventBus**：
```java
public static void register(IEventBus bus) {
    TEST_FUNCTIONS.register(bus);
    bus.addListener(RegisterGameTestsEvent.class, MyClass::onRegisterGameTests);
}
```

**Step 3 — 创建 `FunctionGameTestInstance`**：
```java
private static void onRegisterGameTests(RegisterGameTestsEvent event) {
    // 创建测试环境定义
    Holder<TestEnvironmentDefinition<?>> defaultEnv = event.registerEnvironment(
        Identifier.fromNamespaceAndPath(MOD_ID, "default"),
        new TestEnvironmentDefinition.AllOf()
    );

    // 创建 TestData
    TestData<Holder<TestEnvironmentDefinition<?>>> testData = new TestData<>(
        defaultEnv,
        Identifier.fromNamespaceAndPath("minecraft", "empty"),  // 结构
        100,      // maxTicks
        5,        // setupTicks
        true      // required
    );

    // 创建 FunctionGameTestInstance（包装 DeferredHolder 的 key）
    FunctionGameTestInstance instance = new FunctionGameTestInstance(
        TEST1.getKey(),  // 引用 DeferredHolder 的 ResourceKey
        testData
    );

    // 注册测试
    event.registerTest(
        Identifier.fromNamespaceAndPath(MOD_ID, "test_name"),
        instance
    );
}
```

### 关键 API 说明

| 类型 | 作用 |
|------|------|
| `TestEnvironmentDefinition.AllOf` | 空环境定义（适用于不需要特殊游戏规则的测试） |
| `FunctionGameTestInstance` | 包装一个 `Consumer<GameTestHelper>` 作为游戏测试实例 |
| `TestData` | 包含环境、结构、超时时间等测试元数据 |
| `DeferredHolder.getKey()` | 返回 `ResourceKey`，用于在 RegisterGameTestsEvent 中引用 |
| `RegisterGameTestsEvent.registerEnvironment()` | 注册自定义测试环境 |
| `RegisterGameTestsEvent.registerTest()` | 注册单个测试实例 |

### 注意事项

1. `FunctionGameTestInstance` 构造函数的第一个参数是 `Holder.Reference<Consumer<GameTestHelper>>`，使用 `TEST1.getKey()` 转换为 `ResourceKey` 后由框架自动解析
2. `TestData` 中的 `maxTicks` 设定测试超时，刷取测试需要足够时间（建议 120+ ticks）
3. 测试结构使用 `minecraft:empty` 空结构（不需要 NBT 文件）
4. `setupTicks` 用于在测试开始前等待方块/实体 Tick

---

## Entry 19 — `BrushableBlock.tick()` 内置重力坠落逻辑（M2）

**根本原因**：`BrushableBlock` 的 `tick()` 方法除了调用 `brushable.checkReset(level)` 衰减刷取计数外，还会在下方为空时主动生成 `FallingBlockEntity`。这不是 `FallingBlock` 类的行为，而是 `BrushableBlock` 自身实现的。

**症状**：自定义的可疑方块（继承 `BrushableBlock`）在放入遗迹结构后 2 tick，自动坠落为掉落物。

**错误认知**：认为 `BrushableBlock` 没有重力行为，重力只存在于 `FallingBlock` 继承体系中。

**正确认知**：`BrushableBlock.tick()` (26.1) 的完整逻辑：
```java
public void tick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
    BlockEntity be = level.getBlockEntity(pos);
    if (be instanceof BrushableBlockEntity brushable) {
        brushable.checkReset(level);
    }
    // ⚠️ brushable 沙砾/沙子的重力逻辑在此！
    if (FallingBlock.isFree(level.getBlockState(pos.below())) && pos.getY() >= level.getMinY()) {
        FallingBlockEntity falling = FallingBlockEntity.fall(level, pos, state);
        falling.disableDrop();
    }
}
```

这个设计是因为原版的 `suspicious_sand` 和 `suspicious_gravel` 需要继承基础沙/砂砾的重力行为，但 `BrushableBlock` 不能 extends `FallingBlock`，所以把重力逻辑实现在了 `tick()` 里。

**修复方案**：自定义子类必须重写 `tick()` 以跳过坠落逻辑：
```java
@Override
public void tick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
    BlockEntity be = level.getBlockEntity(pos);
    if (be instanceof RelicBrushableBlockEntity brushable) {
        brushable.checkReset(level);
    }
    // 跳过 FallingBlockEntity.fall() — 我们的方块不坠落
}
```

**触发时序**：`BrushableBlock` 有以下 4 种方式触发 `tick()`：
| 触发方式 | 方法 | 延迟 |
|---|---|---|
| 方块放入世界 | `onPlace()` → `scheduleTick(pos, this, 2)` | 2 ticks |
| 邻居方块变化 | `updateShape()` → `scheduleTick()` | 2 ticks |
| 每次刷取后（未完成） | `BrushableBlockEntity.brush()` → `scheduleTick()` | 2 ticks |
| `checkReset()` 超时重置 | `checkReset()` → `scheduleTick()` | 2 ticks |

**反编译证据**：`net.minecraft.world.level.block.BrushableBlock.tick()` (26.1.1 client jar)

---

## Entry 20 — `brushingCompleted()` 音效与粒子行为（M2）

**根本原因**：刷取完成时只有一种音效（`brushCompletedSound`），没有方块破坏音效。

**症状**：误以为刷取完成时有双重音效。

**正确认知**：`brushingCompleted()` 的完整流程：
1. `dropContent()` — 掉落战利品（无声）
2. `level.levelEvent(3008, pos, Block.getId(state))` — 播放刷取完成音效 + 生成方块破坏粒子（视觉上看起来像方块碎裂，但没有声音）
3. `level.setBlock(pos, turnsInto.defaultBlockState(), 3)` — 替换方块（flag 3 = BLOCK_UPDATE + SYNC_CLIENTS，不发声音）

客户端对 event 3008 的处理：
1. 从方块 ID 获取方块状态
2. 如果是 `BrushableBlock`，调用 `getBrushCompletedSound()` 播放音效
3. 调用 `addDestroyBlockEffect()` 生成破碎粒子（仅视觉）

**结论**：自定义方块的刷取音效通过 `brushCompletedSound` 参数控制，唯一的音效来源。

**反编译证据**：`net.minecraft.world.level.block.entity.BrushableBlockEntity.brushingCompleted()` (26.1.1) + `net.minecraft.client.multiplayer.ClientLevel.levelEvent()` 3008 handler

---

## Entry 21 — `BrushableBlock.animateTick()` 落下粉尘粒子（M2）

**根本原因**：`BrushableBlock` 重写了 `animateTick()`，当方块下方为空时，每 tick 有 1/16 概率生成 `FALLING_DUST` 粒子（使用方块自身纹理）。

**症状**：自定义的可疑方块悬空放置时，底部出现白色粉尘粒子（使用方块纹理渲染），视觉效果与沙子的悬浮粒子完全相同。

**正确认知**：`BrushableBlock.animateTick()` (26.1.1) 的完整逻辑：
```java
@Override
public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
    if (random.nextInt(16) == 0) {
        BlockPos below = pos.below();
        if (FallingBlock.isFree(level.getBlockState(below))) {
            double x = pos.getX() + random.nextDouble();
            double y = pos.getY() - 0.05;
            double z = pos.getZ() + random.nextDouble();
            level.addParticle(new BlockParticleOption(ParticleTypes.FALLING_DUST, state),
                x, y, z, 0.0, 0.0, 0.0);
        }
    }
}
```

粒子使用 `new BlockParticleOption(ParticleTypes.FALLING_DUST, state)`，其中 `state` 是方块自身的 BlockState。所以粒子颜色和纹理取决于自定义方块的材质。

**修复方案**：重写 `animateTick()` 为空方法：
```java
@Override
public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
    // 不调用 super — 阻止落下粉尘粒子
}
```

**反编译证据**：`net.minecraft.world.level.block.BrushableBlock.animateTick()` (26.1.1)

**关联**：配合 Entry 19（`tick()` 重力），两者需要同时重写才能完全消除重力相关行为。

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

---

## M2 第二阶段卡点记录（2026-04-27）

### Entry 22 — ResourceKey 无法调用 .location() 方法（Java 编译错误）

**根本原因**：`ResourceKey<T>` 在 Minecraft 26.1 / Java 25 环境下没有 `location()` 方法。该方法可能存在于旧版本（1.20.x/1.21.x）但已在新版本中被移除或未暴露。编译时报错 `cannot find symbol`。

**症状**：
```
Error: cannot find symbol
  symbol: method location()
  location: variable lootKey of type ResourceKey<LootTable>
```

**错误认知**：
- 认为 `ResourceKey` 有 `location()` 方法返回 `Identifier`
- 认为可以通过 `lootKey.location().equals(...)` 比较战利品表 key

**正确认知**：
`ResourceKey<T>` 在 26.1 中不提供 `location()` 方法。正确的比较方式是直接使用 `.equals()`：

```java
// ✅ 正确：直接比较 ResourceKey 对象
ResourceKey<LootTable> expected = ResourceKey.create(
    Registries.LOOT_TABLE,
    Identifier.fromNamespaceAndPath("relictales", "blocks/suspicious_cracked_stone_bricks")
);
if (expected.equals(acc.relictales$getLootTable())) {
    // 匹配
}

// ❌ 错误：.location() 不存在
if (lootKey.location().equals(Identifier.of("relictales", "blocks/xxx"))) {
```

**替代方案**：如果需要获取 Identifier，使用 `lootKey.location()` —— 实际上在 26.1 中此方法可能是 package-private 或确实不存在。在任何情况下应直接比较 ResourceKey 而非提取 Identifier。

---

### Entry 23 — @Mixin(targets) 访问内部类（`$` 分隔符）

**根本原因**：Minecraft 中的一些结构类（如 `StrongholdPieces.RoomCrossing`、`StrongholdPieces.ChestCorridor` 等）是内部类（inner class），无法直接使用 `@Mixin(ClassName.class)` 引用，因为内部类在 JVM 层面编译为 `OuterClass$InnerClass` 形式。

**症状**：
```
Mixin apply failed — could not find target class
```

**错误认知**：
- 认为可以直接 `@Mixin(StrongholdPieces.RoomCrossing.class)` 引用内部类
- 认为 Mixin 能自动处理内部类的 JVM 名称格式

**正确认知**：

访问内部类必须使用 `@Mixin(targets = "完整类名$内部类名")`，不能直接用 `.class` 引用：

```java
// ✅ 正确：使用 targets 属性 + $ 分隔符
@Mixin(targets = "net...structures.StrongholdPieces$RoomCrossing", remap = false)
public interface RoomCrossingAccessor {
    @Accessor("type")
    int relictales$getType();
}

// ❌ 错误：不能直接引用内部类
@Mixin(StrongholdPieces.RoomCrossing.class, remap = false)
```

**Mixin JSON 中不需要特殊处理**，因为这是 Java 注解层面的问题（编译时解析）。

**适用场景**：任何需要 Mixin 访问原版 Minecraft 内部类（`OuterClass$InnerClass`）的场景。

---

### Entry 24 — 原版可疑方块纹理系统：预烘焙 PNG，无运行时叠加层

**根本原因**：Minecraft 原版可疑方块（suspicious_sand / suspicious_gravel）的裂纹效果**不是在运行时叠加生成的**。每个 dusted 等级（0-3）都有独立预烘焙的 16×16 PNG 纹理。

**错误认知**：
- 认为原版存在某种运行时"裂纹叠加层"系统，可以通过 API 向任意方块添加裂纹纹理
- 以为可以在渲染层面实时叠加裂纹材质

**正确认知**：

| 概念 | 实际情况 |
|------|---------|
| 纹理存储 | 4 个独立 PNG（`suspicious_sand_0~3.png`），非叠加层 |
| 切换机制 | `dusted=N` blockstate → 不同模型引用不同纹理 |
| 方块模型 | 每个等级一个独立模型 JSON |
| 动画效果 | 刷取时递增 `dusted` → 框架自动切换模型/纹理 |

**提取裂纹遮罩的方法**：逐像素对比 suspicious 纹理与基础纹理：
```python
base_img = Image.open("sand.png").convert("RGBA")
susp_img = Image.open("suspicious_sand_0.png").convert("RGBA")
crack_positions = set()
for y in range(16):
    for x in range(16):
        if base_px[x, y] != susp_px[x, y]:
            crack_positions.add((x, y))
```

**生成的裂纹数据**（151 个唯一位置，从 sand+gravel 联合提取）：
| 等级 | 累积裂纹数 |
|------|-----------|
| 0 | 72 |
| 1 | 93 |
| 2 | 118 |
| 3 | 151 |

**验证方式**：生成自定义纹理 + `dusted=N` blockstate + 分等级 block model，Minecraft 原生支持多级纹理切换，无需任何渲染代码。

**关联工具**：`tools/generate_suspicious_textures.py`

---

### Entry 25 — 要塞结构注入：MixinStructurePiece 拦截 placeBlock() 实现概率替换

**根本原因**：要塞（Stronghold）是 Jigsaw 结构，本可使用 StructureProcessor。但由于 MixinStructurePiece 方案更灵活（支持按房间类型/位置设置不同概率），最终采用 Mixin 方案。

**设计要点**：

**拦截点**：`StructurePiece.placeBlock()` HEAD（要塞的所有子片都继承此方法）
```java
@Mixin(value = StructurePiece.class, remap = false)
public abstract class MixinStructurePiece {
    @Inject(method = "placeBlock", at = @At("HEAD"), cancellable = true, remap = false)
    private void relictales$onPlaceBlock(
            WorldGenLevel level, BlockState state, int x, int y, int z,
            BoundingBox chunkBB, CallbackInfo ci) {
```

**概率系统**（按房间类型 × 位置 × 方块类型）：
| 房间 | 位置 | 方块 | 概率 |
|------|------|------|------|
| Library | 全部 | 裂纹/苔石砖 | 10% |
| RoomCrossing | 中心柱 (5,1,5) | 石砖/裂纹砖 | 100% |
| RoomCrossing | 中心 3×3 地板 | 裂纹/苔石砖 | 50% |
| RoomCrossing | 其他 | 裂纹/苔石砖 | 10% |
| FiveCrossing | 全部 | 裂纹/苔石砖 | 10% |
| ChestCorridor | 中心地板 | 裂纹/苔石砖 | 100% |
| ChestCorridor | 其他 | 裂纹/苔石砖 | 6% |
| PortalRoom | 全部 | 裂纹/苔石砖 | 6% |
| 其他房间 | 全部 | 裂纹/苔石砖 | 1% |

**RoomCrossing 类型区分**：通过 `@Accessor("type")` 读取 `RoomCrossing.type` 字段（0=柱厅, 1=喷泉, 2=储藏室）。

**战利品表注入延迟**：使用 `level.getLevel()`（而非 `instanceof ServerLevel`）解决 WorldGenLevel 无法直接设置 loot table 的问题，通过 server tick 延迟执行。

**联合提取**：从原版可疑沙砾（151 裂纹位置）和可疑沙子（148 裂纹位置）联合提取裂纹位置并集，确保裂纹遮罩兼容两种原版纹理风格。

---

## Entry 26 — 下界要塞 Mixin 注入（空气暴露检测 + 按楼层概率衰减）

**背景**：为下界要塞添加可疑方块注入，沿用 MixinStructurePiece 的 `StructurePiece.placeBlock()` HEAD 拦截模式。

**关键挑战**：下界要塞是用 `NETHER_BRICKS` 构建的巨型结构（≈25K+ 方块），比要塞大得多。如果所有空气暴露的 NETHER_BRICKS 都以相同概率替换，会产生过量嫌疑方块。

**解决方案**：

### 1. 单一 Mixin 多分支共存

要塞和下界要塞共享同一个 `MixinStructurePiece`，通过 `getDeclaringClass()` 分支：

```java
Class<?> declaring = self.getClass().getDeclaringClass();
if (declaring == StrongholdPieces.class) {
    handleStronghold(level, state, x, y, z, chunkBB, ci, self);
} else if (declaring == NetherFortressPieces.class) {
    handleNetherFortress(level, state, x, y, z, chunkBB, ci, self);
}
```

不需要创建两个 Mixin 同时注入 `StructurePiece.placeBlock()`（那样会冲突）。

### 2. 空气暴露检测（避免替换埋墙方块）

```java
private static boolean isAirExposed(WorldGenLevel level, BlockPos pos) {
    for (Direction dir : Direction.values()) {
        if (level.getBlockState(pos.relative(dir)).isAir()) return true;
    }
    return false;
}
```

在 `placeBlock` 拦截时检查 6 方向邻居。利用 `generateBox` 的循环顺序：同一 generateBox 调用内的块在循环过程中会有部分已放置的邻居。墙体内的块最终会被其他 NETHER_BRICKS 包围，不会被误判为暴露。

### 3. 按楼层 Y 值概率衰减

针对 CastlStalkRoom 等大房间的 floor/wall 区分：

```java
if (piece instanceof NetherFortressPieces.CastleStalkRoom) {
    // Floor y=3-4 (2 layers) → full 10%
    // Wall  y=5+  (8 layers) → reduced 2%
    return y <= 4 ? 0.10f : 0.02f;
}
```

**为什么需要**：CastleStalkRoom 是 13×14×13 的巨型房间，仅 floor 层 y=3-4 两层是玩家行走面。墙壁从 y=5 到 y=12 共 8 层，且全部空气暴露。如果 floor 和 wall 同概率，wall 块数量是 floor 的 4×，导致墙面积累大量嫌疑方块，视觉上喧宾夺主。

**适用房间**：
| 房间 | 楼层 Y | 墙面 Y | 楼层概率 | 墙面概率 |
|------|--------|--------|---------|---------|
| CastleStalkRoom | y≤4 | y≥5 | 10% | 2% |
| MonsterThrone | y≤1 | y≥2 | 30% | 10% |

### 4. 特殊位置 100% 替换

熔岩井（CastleEntrance）底部的浮空下界砖 `local(6,0,6)` 被强制替换：

```java
if (isNetherLavaWellBottom(self, x, y, z)) {
    // 100% replacement, bypasses chance and air-exposed check
}
```

### 5. 下界要塞概率表

| 房间 | 概率 | 备注 |
|------|------|------|
| MonsterThrone | 30%/10% | 小房间，floor/wall 分层 |
| CastleStalkRoom | 10%/2% | 大房间，floor/wall 分层 |
| StairsRoom | 5% | — |
| CastleCorridorStairs | 5% | — |
| CastleCorridorTBalcony | 4% | — |
| CastleEntrance / RoomCrossing / BridgeCrossing / Crossing | 3% | 熔岩井底 100% |
| 小走廊/转弯/BridgeStraight | 1% | — |
| 全覆盖兜底 | 0.2% | — |

**原理**：下界要塞是露天巨型开放结构，可视区块比例远高于要塞，因此单体概率低 10-50×，但总暴露面积更大，实际生成数量仍合理。

---

*沉淀时间：2026-04-28*
*来源项目：RelicTales (RelicTales)*
