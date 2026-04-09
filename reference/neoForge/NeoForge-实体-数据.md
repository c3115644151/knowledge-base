# NeoForge 实体数据与网络同步

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/entities/data

## 概述

实体数据系统用于在实体的生命周期内存储和同步数据。NeoForge 提供了 `SynchedEntityData` 用于客户端-服务端同步，`Data Attachments` 用于扩展数据存储。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `SynchedEntityData` | 同步实体数据 |
| `EntityDataAccessor<T>` | 数据访问器 |
| `EntityDataSerializer<T>` | 数据序列化器 |
| `EntityDataSerializers` | 内置序列化器 |

### 内置序列化器

| 序列化器 | 类型 |
|----------|------|
| `BYTE` | `byte` |
| `INT` | `int` |
| `FLOAT` | `float` |
| `STRING` | `String` |
| `ITEM_STACK` | `ItemStack` |
| `BLOCK_POS` | `BlockPos` |
| `OPTIONAL_BLOCK_POS` | `Optional<BlockPos>` |
| `BOOLEAN` | `boolean` |
| `ROTATION` | `Vector3f` |

---

## 代码示例

### 基本同步数据

```java
public class MyEntity extends Entity {
    // 1. 定义数据访问器
    public static final EntityDataAccessor<Integer> DATA_ID = 
        SynchedEntityData.defineId(
            MyEntity.class,
            EntityDataSerializers.INT
        );
    
    public static final EntityDataAccessor<Boolean> DATA_FLAG = 
        SynchedEntityData.defineId(
            MyEntity.class,
            EntityDataSerializers.BOOLEAN
        );
    
    public static final EntityDataAccessor<Optional<Component>> 
        DATA_CUSTOM_NAME = 
        SynchedEntityData.defineId(
            MyEntity.class,
            EntityDataSerializers.OPTIONAL_COMPONENT
        );
    
    // 2. 定义默认值
    @Override
    protected void defineSynchedData(
            SynchedEntityData.Builder builder) {
        builder.define(DATA_ID, 0);
        builder.define(DATA_FLAG, false);
        builder.define(DATA_CUSTOM_NAME, Optional.empty());
    }
    
    // 3. 访问数据
    public int getMyData() {
        return this.getEntityData().get(DATA_ID);
    }
    
    public void setMyData(int value) {
        this.getEntityData().set(DATA_ID, value);
    }
    
    public boolean isFlagged() {
        return this.getEntityData().get(DATA_FLAG);
    }
    
    // 4. 标记脏数据（强制同步）
    public void incrementData() {
        this.getEntityData().set(DATA_ID, 
            this.getMyData() + 1, 
            true);  // 第二个参数为 true 时标记脏
    }
}
```

### 持久化数据（存档）

```java
public class MyEntity extends Entity {
    private int savedData;
    
    @Override
    protected void readAdditionalSaveData(ValueInput input) {
        // 从存档读取数据
        this.savedData = input.getIntOr("my_data", 0);
        
        // 读取可选数据
        input.getString("my_name")
            .ifPresent(name -> {
                // 处理数据
            });
    }
    
    @Override
    protected void addAdditionalSaveData(ValueOutput output) {
        // 保存数据到存档
        output.putInt("my_data", this.savedData);
        output.putString("my_name", "Example");
    }
    
    @Override
    public void addAdditionalSaveData(
            CompoundTag compound) {
        // 旧版方法，仍可用但推荐使用 Value I/O
        compound.putInt("my_data", this.savedData);
    }
}
```

### 自定义 Spawn 数据

```java
public class MyEntity extends Entity implements IEntityWithComplexSpawn {
    private int spawnData;
    
    @Override
    public void writeSpawnData(
            RegistryFriendlyByteBuf buf) {
        // 写入生成时的数据
        buf.writeInt(this.spawnData);
        buf.writeEnum(InitType.EXAMPLE);
    }
    
    @Override
    public void readSpawnData(
            RegistryFriendlyByteBuf buf) {
        // 读取生成时的数据（仅客户端）
        this.spawnData = buf.readInt();
        InitType type = buf.readEnum(InitType.class);
        // 初始化客户端状态
    }
    
    @Override
    public void sendPairingData(
            ServerPlayer player, 
            Consumer<CustomPacketPayload> packetConsumer) {
        // 发送配对数据
        super.sendPairingData(player, packetConsumer);
        
        // 发送自定义数据包
        packetConsumer.accept(
            new ExampleEntityPacket(this.getId(), this.spawnData)
        );
    }
}
```

### 数据附件 (Data Attachments)

```java
// 1. 定义 AttachmentType
public static final AttachmentType<Integer> MY_ATTACHMENT = 
    AttachmentType.builder(
        () -> 0  // 默认值
    ).build();

public static final AttachmentType<ItemStack> EQUIPMENT = 
    AttachmentType.<ItemStack>builder(
        () -> ItemStack.EMPTY
    ).build();

public static final AttachmentType<Collection<MobEffectInstance>> 
    ACTIVE_EFFECTS = 
    AttachmentType.<Collection<MobEffectInstance>>builder(
        ArrayList::new  // 使用工厂方法
    ).build();

// 2. 注册 AttachmentType
private static final DeferredRegister<AttachmentType<?>> 
    ATTACHMENT_TYPES = 
    DeferredRegister.create(
        NeoForgeRegistries.Keys.ATTACHMENT_TYPES, MOD_ID);

public static final DeferredHolder<AttachmentType<?>, 
        AttachmentType<Integer>> MY_ATTACHMENT = 
    ATTACHMENT_TYPES.register("my_attachment", () -> 
        AttachmentType.builder(() -> 0).build());

// 3. 在实体上使用
public class MyEntity extends Entity {
    @Override
    protected void defineAttachments(
            RegistrationInfo info) {
        // 定义此实体支持的附件
        this.defineData(MY_ATTACHMENT, 42);  // 自定义默认值
    }
    
    public int getMyValue() {
        return this.getData(MY_ATTACHMENT);
    }
    
    public void setMyValue(int value) {
        this.setData(MY_ATTACHMENT, value);
    }
}

// 4. 同步到客户端
public static final AttachmentType<Integer> SYNCED_ATTACHMENT = 
    AttachmentType.<Integer>builder(() -> 0)
        .sync((entity, value, dist) -> {
            // 同步回调
            return value;
        })
        .build();
```

### 自定义 EntityDataSerializer

```java
// 1. 创建自定义序列化器
public class Vector3iSerializer 
        implements EntityDataSerializer<Vector3i> {
    @Override
    public void write(FriendlyByteBuf buf, Vector3i value) {
        buf.writeInt(value.getX());
        buf.writeInt(value.getY());
        buf.writeInt(value.getZ());
    }
    
    @Override
    public Vector3i read(FriendlyByteBuf buf) {
        return new Vector3i(
            buf.readInt(),
            buf.readInt(),
            buf.readInt()
        );
    }
    
    @Override
    public void writeJson(Vector3i value, JsonObject json) {
        json.addProperty("x", value.getX());
        json.addProperty("y", value.getY());
        json.addProperty("z", value.getZ());
    }
    
    @Override
    public Vector3i readJson(JsonObject json) {
        return new Vector3i(
            JsonHelper.getInt(json, "x"),
            JsonHelper.getInt(json, "y"),
            JsonHelper.getInt(json, "z")
        );
    }
}

// 2. 注册序列化器
@Mod.EventBusSubscriber(modid = MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public static class Registries {
    public static final EntityDataSerializer<Vector3i> 
        VECTOR_3I = new Vector3iSerializer();
    
    @SubscribeEvent
    public static void register(
            RegisterEntityDataSerializerEvent event) {
        event.register(VECTOR_3I);
    }
}
```

---

## 注意事项

### 同步策略
- `SynchedEntityData`：自动同步到客户端
- `AttachmentType`：需要显式定义 `sync` 回调
- 频繁更新的数据使用 `EntityDataAccessor` 更高效

### 常见错误
1. **数据不同步**：忘记在 `defineSynchedData` 中定义默认值
2. **空指针异常**：访问未定义的数据访问器
3. **性能问题**：高频更新的数据可能造成网络拥塞

### 最佳实践

```java
// 推荐：使用 record 存储数据
public record EntityData(int health, int mana) {
    public static final EntityData DEFAULT = new EntityData(20, 100);
}

// 或者使用实体数据类
public static class MyEntityData {
    public int health = 20;
    public int mana = 100;
}
```

---

## 关联引用

- 实体基础：[NeoForge-实体](./NeoForge-实体.md)
- LivingEntity：[NeoForge-实体-LivingEntity](./NeoForge-实体-LivingEntity.md)
- 网络通信：[NeoForge-网络-Payload](./NeoForge-网络-Payload.md)
- 数据存储：[NeoForge-数据存储-附件](./NeoForge-数据存储-附件.md)
