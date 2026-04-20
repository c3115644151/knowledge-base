# NeoForge 方块开发

## 注册方块

### 基本注册流程

```java
// 1. 创建 DeferredRegister
public static final DeferredRegister.Blocks BLOCKS =
    DeferredRegister.createBlocks(MOD_ID);

// 2. 注册方块
public static final DeferredBlock<Block> EXAMPLE_BLOCK = BLOCKS.register(
    "example_block",
    registryName -> new Block(
        BlockBehaviour.Properties.of()
            .setId(ResourceKey.create(Registries.BLOCK, registryName))
            .destroyTime(2.0f)
            .explosionResistance(10.0f)
            .sound(SoundType.GRAVEL)
            .lightLevel(state -> 7)
    )
);

// 3. 在 Mod 构造函数中注册
public ExampleMod(IEventBus modBus) {
    ModBlocks.BLOCKS.register(modBus);
}
```

### BlockBehaviour.Properties 常用方法

| 方法 | 说明 | 示例值 |
|------|------|--------|
| `setId()` | 设置资源键（**必须**） | - |
| `destroyTime(float)` | 破坏时间 | 石头1.5, 泥土0.5, 黑曜石50 |
| `explosionResistance(float)` | 爆炸抗性 | 石头6.0, 黑曜石1200 |
| `sound(SoundType)` | 音效 | SoundType.STONE |
| `lightLevel(Function)` | 发光等级(0-15) | 发光石头→15 |
| `friction(float)` | 摩擦力 | 冰→0.98 |
| `isValidSpawn(BlockBehaviour$BoDiagonal)` | 生物生成判定 | - |
| `noOcclusion()` | 无碰撞箱遮挡 | - |
| `noLootTable()` | 无战利品表 | - |

### DeferredRegister.Blocks 辅助方法

```java
// 自动设置 setId
public static final DeferredBlock<Block> BLOCK = BLOCKS.register(
    "block_name",
    Block::new,
    props -> props.destroyTime(1.0f)
);
```

---

## 自定义方块类

```java
public class CustomBlock extends Block {
    public CustomBlock() {
        super(BlockBehaviour.Properties.of()
            .setId(ResourceKey.create(Registries.BLOCK,
                Identifier.fromNamespaceAndPath(MOD_ID, "custom_block")))
            .destroyTime(1.5f)
        );
    }

    @Override
    protected void interactWithBlock(
            BlockState state,
            Level level,
            BlockPos pos,
            Player player,
            InteractionHand hand,
            BlockHitResult hitResult) {
        // 右键交互逻辑
        if (!level.isClientSide()) {
            // 服务端逻辑
        }
        super.interactWithBlock(state, level, pos, player, hand, hitResult);
    }
}
```

### 常用方法重写

```java
// 方块状态变化时调用
@Override
public void neighborChanged(
    BlockState state,
    Level level,
    BlockPos pos,
    Block block,
    BlockPos fromPos,
    boolean isMoving) {
    // 充能/信号更新等
}

// 生物破坏方块时调用
@Override
public void playerWillDestroy(
    Level level,
    BlockPos pos,
    BlockState state,
    Player player) {
    // 自定义掉落逻辑
    super.playerWillDestroy(level, pos, state, player);
}

// 设置渲染覆盖（无模型渲染）
@Override
public RenderShape getRenderShape(BlockState state) {
    return RenderShape.INVISIBLE;
}
```

---

## 方块状态 (BlockState)

### 获取与检查

```java
// 获取方块状态
BlockState state = level.getBlockState(pos);

// 检查方块
if (state.is(Blocks.DIRT)) { }
if (state.is(MyBlocks.MY_BLOCK.get())) { }

// 检查属性
if (state.getValue(BlockStateProperties.FACING) == Direction.NORTH) { }
```

### 常见 BlockStateProperties

| 属性 | 类型 | 获取方法 |
|------|------|----------|
| `HORIZONTAL_FACING` | Direction | `getValue(BlockStateProperties.HORIZONTAL_FACING)` |
| `FACING` | Direction | `getValue(BlockStateProperties.FACING)` |
| `POWERED` | boolean | `getValue(BlockStateProperties.POWERED)` |
| `WATERLOGGED` | boolean | `getValue(BlockStateProperties.WATERLOGGED)` |
| `AXIS` | Direction.Axis | `getValue(BlockStateProperties.AXIS)` |

### 创建方块状态属性

```java
// 在方块类中定义
public static final BooleanProperty ACTIVATED = BooleanProperty.create("activated");
public static final IntProperty POWER = IntegerProperty.create("power", 0, 15);
public static final EnumProperty<Direction> FACING =
    EnumProperty.create("facing", Direction.class);

// 使用属性
@Override
protected void createBlockStateDefinition(
        StateDefinition.Builder<Block, BlockState> builder) {
    builder.add(ACTIVATED, POWER, FACING);
}

// 获取默认状态
@Override
protected BlockState defaultBlockState() {
    return this.stateDefinition.any()
        .setValue(ACTIVATED, false)
        .setValue(POWER, 0)
        .setValue(FACING, Direction.NORTH);
}

// 处理属性变化
@Override
public BlockState getStateForPlacement(BlockPlaceContext context) {
    return this.defaultBlockState()
        .setValue(FACING, context.getNearestLookingDirection().getOpposite());
}

@Override
public BlockState mirror(BlockState state, Mirror mirror) {
    return state.rotate(mirror.getRotation(state.getValue(FACING)));
}

@Override
public BlockState rotate(BlockState state, Rotation rotation) {
    return state.setValue(FACING, rotation.rotate(state.getValue(FACING)));
}
```

---

## 方块实体 (BlockEntity)

### 快速创建流程

```java
// 1. 创建方块实体类
public class MyBlockEntity extends BlockEntity {
    public MyBlockEntity(BlockEntityType<?> type, BlockPos pos, BlockState state) {
        super(type, pos, state);
    }
}

// 2. 注册 BlockEntityType
public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITY_TYPES =
    DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE, MOD_ID);

public static final Supplier<BlockEntityType<MyBlockEntity>> MY_BLOCK_ENTITY =
    BLOCK_ENTITY_TYPES.register("my_block_entity", () ->
        new BlockEntityType<>(
            MyBlockEntity::new,
            false,  // opPlayersOnly for NBT loading
            MyBlocks.MY_BLOCK.get()  // 关联的方块
        )
    );

// 3. 实现 EntityBlock 接口
public class MyEntityBlock extends Block implements EntityBlock {
    @Override
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new MyBlockEntity(MY_BLOCK_ENTITY.get(), pos, state);
    }

    // Ticker 支持
    @Override
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(
            Level level, BlockState state, BlockEntityType<T> type) {
        return createTickerHelper(type, MY_BLOCK_ENTITY.get(), MyBlockEntity::tick);
    }
}
```

### 数据存储

```java
public class MyBlockEntity extends BlockEntity {
    private int counter;

    @Override
    public void loadAdditional(ValueInput input) {
        super.loadAdditional(input);
        this.counter = input.getIntOr("counter", 0);
    }

    @Override
    public void saveAdditional(ValueOutput output) {
        super.saveAdditional(output);
        output.putInt("counter", this.counter);
    }
}
```

⚠️ 修改数据后必须调用 `setChanged()` 标记脏chunk！

### Ticker

```java
// 方块中
private static <E extends BlockEntity, A extends BlockEntity>
    @Nullable BlockEntityTicker<A> createTickerHelper(
    BlockEntityType<A> type, BlockEntityType<E> checkedType,
    BlockEntityTicker<? super E> ticker) {
    return checkedType == type ? (BlockEntityTicker<A>) ticker : null;
}

@Override
public <T extends BlockEntity> BlockEntityTicker<T> getTicker(...) {
    return createTickerHelper(type, MY_BLOCK_ENTITY.get(), MyBlockEntity::tick);
}

// BlockEntity 中
public static void tick(
        Level level, BlockPos pos, BlockState state,
        MyBlockEntity blockEntity) {
    // 每tick执行逻辑
}
```

### 同步到客户端

#### 方式1: Chunk加载时同步
```java
@Override
public CompoundTag getUpdateTag(HolderLookup.Provider registries) {
    return this.saveWithoutMetadata(registries);
}
```

#### 方式2: 方块更新时同步
```java
@Override
public Packet<ClientGamePacketListener> getUpdatePacket() {
    return ClientboundBlockEntityDataPacket.create(this);
}

// 触发同步
level.sendBlockUpdated(pos, state, state, 3);
```

#### 方式3: 自定义数据包
```java
// 使用 PacketDistributor
PacketDistributor.sendToPlayersTrackingChunk(
    serverLevel,
    chunkPos,
    new MyPacket(data)
);
```

---

## BrushableBlock（可疑方块 / 考古）

> 用于注入原版遗迹的可疑方块，继承自 `BrushableBlock` 复用原版考古机制。

### 注册语法（26.1 正确版本）

⚠️ **常见错误**：
- ❌ 使用三参数 `registerBlock(name, lambda, props)` —— 该重载在 1.21.10 已废弃
- ❌ 使用 `BlockBehaviour.Properties.ofFullCopy(...)` 传参给 `registerBlock`
- ✅ 使用**双参数** `register(name, props -> new Block(...))`

```java
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.BrushableBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.neoforge.registries.DeferredBlock;

import static com.examplemod.init.ModBlocks.BLOCKS;

public class ModBlocks {
    // ✅ 正确：双参数 register，props 由 NeoForge 自动注入
    public static final DeferredBlock<BrushableBlock> SUSPICIOUS_MOSSY_BRICKS = BLOCKS.register(
            "suspicious_mossy_stone_bricks",
            props -> new BrushableBlock(
                    Blocks.MOSSY_STONE_BRICKS,  // 刷取完成后变回的方块
                    SoundEvents.BRUSH_GENERIC,   // 刷取中音效（无 GENERIC_COMPLETED）
                    SoundEvents.BRUSH_GRAVEL_COMPLETED, // 刷取完成音效
                    props                          // NeoForge 自动注入带 ID 的 properties
            )
    );
}
```

### 为可疑方块注册 BlockItem（26.1 正确写法）

```java
// 正确：使用两参数 register，id 由 NeoForge 注入
public static DeferredItem<BlockItem> MY_BLOCK_ITEM;

public static void init() {
    MY_BLOCK_ITEM = ITEMS.register(
        "my_block",
        id -> new BlockItem(
            MY_BLOCK.get(),
            new Item.Properties().setId(ResourceKey.create(Registries.ITEM, id))
        )
    );
}
```

⚠️ **常见错误**：
- ❌ `new Item.Properties()` 不设置 ID → "Item id not set"
- ❌ 在静态初始化器中调用 `.get()` → "Cannot register after RegisterEvent"

### LootTable 配置

`BrushableBlock` 本身不携带掉落物，必须通过 DataGen 生成 LootTable：

- 文件路径：`data/<modid>/loot_tables/blocks/<block_name>.json`
- Context 类型：`LootContextParamSets.ARCHAEOLOGY`（通过 DataGen 自动设置）

在 `BlockLootSubProvider` 中：
```java
// DataGen 方式
@Override
protected void generate() {
    // BrushableBlock 默认掉落（无自定义 loot 则为空）
    add(ModBlocks.SUSPICIOUS_BLOCK.get(), BlockLootSubProvider::createSingleItemTable);
}
```

## 常见问题

### 何时使用 BlockState vs BlockEntity？

| BlockState | BlockEntity |
|------------|-------------|
| 有限状态（几百个以内） | 无限/大量状态 |
| 静态数据 | 动态数据 |
| 无需每tick处理 | 需要每tick处理 |

### 常见错误

- ❌ 在注册外创建 `new Block()`
- ❌ 修改数据后忘记调用 `setChanged()`
- ❌ 在服务端逻辑中检查 `isClientSide()` 不当
- ❌ BlockEntity 不安全检查导致空指针

## 关联文档
- [NeoForge-方块实体.md](./NeoForge-方块实体.md) - 详细BlockEntity
- [NeoForge-概念.md](./NeoForge-概念.md) - 注册表与事件
