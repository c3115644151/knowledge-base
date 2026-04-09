# NeoForge 方块实体 (Block Entity)

## 概述
BlockEntity 用于在方块上存储无法用 BlockState 表示的数据（如物品栏内容、进度、能量值等）。

### BlockState vs BlockEntity

| BlockState | BlockEntity |
|------------|-------------|
| 有限状态（≤几百个） | 无限/大量状态 |
| 无需每tick更新 | 可每tick更新 |
| 自动保存 | 需手动调用 `setChanged()` |
| 简单数据 | 复杂数据（物品栏、TE） |

---

## 创建与注册

### 1. BlockEntity 类

```java
public class MyBlockEntity extends BlockEntity {
    private int counter;
    
    public MyBlockEntity(
            BlockEntityType<?> type, 
            BlockPos pos, 
            BlockState state) {
        super(type, pos, state);
    }
    
    // 读取数据（从存档/网络）
    @Override
    public void loadAdditional(ValueInput input) {
        super.loadAdditional(input);
        this.counter = input.getIntOr("counter", 0);
    }
    
    // 保存数据
    @Override
    public void saveAdditional(ValueOutput output) {
        super.saveAdditional(output);
        output.putInt("counter", this.counter);
    }
}
```

### 2. 注册 BlockEntityType

```java
public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITY_TYPES =
    DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE, MOD_ID);

public static final Supplier<BlockEntityType<MyBlockEntity>> MY_BLOCK_ENTITY_TYPE =
    BLOCK_ENTITY_TYPES.register("my_block_entity", () ->
        new BlockEntityType<>(
            MyBlockEntity::new,    // 工厂方法
            false,                 // opPlayersOnly for NBT loading
            MyBlocks.MY_BLOCK.get()  // 关联的方块
        )
    );
```

### 3. 实现 EntityBlock

```java
public class MyEntityBlock extends Block implements EntityBlock {
    public MyEntityBlock() {
        super(BlockBehaviour.Properties.of().noOcclusion());
    }
    
    // 创建 BlockEntity
    @Override
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new MyBlockEntity(MY_BLOCK_ENTITY_TYPE.get(), pos, state);
    }
    
    // Ticker 支持（可选）
    @Override
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(
            Level level, 
            BlockState state, 
            BlockEntityType<T> type) {
        return createTickerHelper(type, MY_BLOCK_ENTITY_TYPE.get(), 
            MyBlockEntity::tick);
    }
    
    // Ticker 辅助方法
    private static <E extends BlockEntity, A extends BlockEntity> 
            @Nullable BlockEntityTicker<A> createTickerHelper(
            BlockEntityType<A> type, 
            BlockEntityType<E> checkedType, 
            BlockEntityTicker<? super E> ticker) {
        return checkedType == type ? (BlockEntityTicker<A>) ticker : null;
    }
}
```

### 4. 注册到 Mod 构造函数

```java
@Mod("examplemod")
public class ExampleMod {
    public ExampleMod(IEventBus modBus) {
        MyBlocks.BLOCKS.register(modBus);
        ModBlockEntities.BLOCK_ENTITY_TYPES.register(modBus);
    }
}
```

---

## 多方块关联

```java
public static final Supplier<BlockEntityType<MyBlockEntity>> MY_BLOCK_ENTITY =
    BLOCK_ENTITY_TYPES.register("my_block_entity", () ->
        new BlockEntityType<>(
            MyBlockEntity::new,
            false,
            MyBlocks.BLOCK_1.get(),
            MyBlocks.BLOCK_2.get(),
            MyBlocks.BLOCK_3.get()
        )
    );
```

---

## 数据存储

### ValueIO 方式

```java
public class MyBlockEntity extends BlockEntity {
    private int counter;
    private boolean activated;
    
    @Override
    public void loadAdditional(ValueInput input) {
        super.loadAdditional(input);
        this.counter = input.getIntOr("counter", 0);
        this.activated = input.getBooleanOr("activated", false);
    }
    
    @Override
    public void saveAdditional(ValueOutput output) {
        super.saveAdditional(output);
        output.putInt("counter", this.counter);
        output.putBoolean("activated", this.activated);
    }
    
    // 修改数据后必须调用
    public void incrementCounter() {
        this.counter++;
        this.setChanged();
    }
}
```

⚠️ **重要**: 修改数据后必须调用 `setChanged()` 标记 chunk 为脏！

### 数据附件 (Data Attachments)
适用于向已有 BlockEntity 附加数据：
```java
blockEntity.setData(ATTACHMENT_KEY, new DataValue());
DataValue data = blockEntity.getData(ATTACHMENT_KEY);
```

---

## Ticker（每Tick处理）

### BlockEntity 中的 Tick 方法

```java
public class MyBlockEntity extends BlockEntity {
    public static void tick(
            Level level, 
            BlockPos pos, 
            BlockState state, 
            MyBlockEntity blockEntity) {
        // 每tick执行的逻辑
        blockEntity.counter++;
        if (blockEntity.counter % 20 == 0) {
            // 每秒执行
        }
        blockEntity.setChanged();
    }
}
```

### 仅服务端 Ticker

```java
@Override
public <T extends BlockEntity> BlockEntityTicker<T> getTicker(
        Level level, BlockState state, BlockEntityType<T> type) {
    // 只在服务端执行
    if (level.isClientSide()) return null;
    return createTickerHelper(type, MY_BLOCK_ENTITY_TYPE.get(), 
        MyBlockEntity::tick);
}
```

### 仅客户端 Ticker

```java
@Override
public <T extends BlockEntity> BlockEntityTicker<T> getTicker(
        Level level, BlockState state, BlockEntityType<T> type) {
    // 只在客户端执行
    if (!level.isClientSide()) return null;
    return createTickerHelper(type, MY_BLOCK_ENTITY_TYPE.get(), 
        MyBlockEntity::clientTick);
}
```

---

## 同步到客户端

### 方式1: Chunk 加载时同步

```java
@Override
public CompoundTag getUpdateTag(HolderLookup.Provider registries) {
    return this.saveWithoutMetadata(registries);
}

@Override
public void handleUpdateTag(ValueInput input) {
    super.handleUpdateTag(input);
}
```

### 方式2: 方块更新时同步（推荐）

```java
@Override
public Packet<ClientGamePacketListener> getUpdatePacket() {
    return ClientboundBlockEntityDataPacket.create(this);
}

@Override
public void onDataPacket(Connection connection, ValueInput input) {
    super.onDataPacket(connection, input);
    // 处理接收到的数据
}

// 触发同步
level.sendBlockUpdated(pos, state, state, 3);
```

### 方式3: 自定义数据包

```java
// 发送数据包
PacketDistributor.sendToPlayersTrackingChunk(
    serverLevel, 
    chunkPos, 
    new MyBlockEntitySyncPacket(pos, data)
);
```

⚠️ 接收端必须检查 BlockEntity 是否存在！

---

## 移除处理

### 移除前的数据导出

```java
@Override
public void preRemoveSideEffects(BlockPos pos, BlockState state) {
    super.preRemoveSideEffects(pos, state);
    // 掉落物品、导出数据等
    if (this.hasInventory) {
        Containers.dropContents(level, pos, inventory);
    }
}
```

### 邻居方块更新

```java
public class MyEntityBlock extends Block implements EntityBlock {
    @Override
    protected void affectNeighborsAfterRemoval(
            BlockState state, 
            ServerLevel level, 
            BlockPos pos, 
            boolean movedByPiston) {
        Containers.updateNeighboursAfterDestroy(state, level, pos);
    }
}
```

⚠️ 使用 `Block.UPDATE_SKIP_BLOCK_ENTITY_SIDEEFFECTS` 移除的方块不会触发 `preRemoveSideEffects`！

---

## 物品栏集成

### 实现 Container

```java
public class MyBlockEntity extends BlockEntity implements Container {
    private NonNullList<ItemStack> items;
    
    public MyBlockEntity(...) {
        super(...);
        this.items = NonNullList.withSize(9, ItemStack.EMPTY);
    }
    
    @Override
    public NonNullList<ItemStack> getItems() {
        return items;
    }
    
    @Override
    public int getContainerSize() {
        return items.size();
    }
    
    @Override
    public ItemStack getItem(int slot) {
        return items.get(slot);
    }
    
    @Override
    public ItemStack removeItem(int slot, int count) {
        ItemStack stack = items.get(slot);
        if (stack.isEmpty()) return ItemStack.EMPTY;
        items.set(slot, stack.is(count));
        return stack.split(count);
    }
    
    @Override
    public void setItem(int slot, ItemStack stack) {
        items.set(slot, stack);
    }
    
    @Override
    public boolean canTakeItem(
            Container target, int slot, ItemStack stack) {
        return true;
    }
    
    @Override
    public boolean canPlaceItem(int slot, ItemStack stack) {
        return true;
    }
}
```

实现 `Container` 后，BlockEntity 被破坏时会自动掉落内容物。

---

## 常见问题

### 获取 BlockEntity

```java
// 从方块获取
BlockEntity be = level.getBlockEntity(pos);
if (be instanceof MyBlockEntity myBE) {
    // 使用
}

// 安全检查
if (level.hasChunkAt(pos)) {
    BlockEntity be = level.getBlockEntity(pos);
    if (be != null && !be.isRemoved()) {
        // 使用
    }
}
```

### BlockEntity 类型转换

```java
@Nullable
MyBlockEntity be = level.getBlockEntity(pos) instanceof MyBlockEntity mbe 
    ? mbe : null;

if (be != null) {
    be.incrementCounter();
}
```

### 生命周期问题

- ❌ BlockEntity 在 Chunk 卸载时可能被移除
- ❌ 不要在 Chunk 未加载时尝试同步
- ❌ 使用前检查 `!blockEntity.isRemoved()`

## 关联文档
- [NeoForge-方块.md](./NeoForge-方块.md) - 方块开发基础
- [NeoForge-网络.md](./NeoForge-网络.md) - 自定义数据包同步
