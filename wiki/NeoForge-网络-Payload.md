# NeoForge 网络 Payload 系统

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/networking/payload

## 概述

Payload 系统用于在客户端和服务端之间发送自定义网络数据包。每个 Payload 都有对应的编解码器用于序列化和反序列化。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `CustomPacketPayload` | 自定义数据包接口 |
| `PayloadType` | Payload 类型定义 |
| `PayloadRegistrar` | Payload 注册器 |
| `FriendlyByteBuf` | 友好字节缓冲区 |
| `PacketDistributor` | 数据包分发器 |

### 线程上下文

| 值 | 说明 |
|----|------|
| `PLAY` | 主线程运行 |
| `LOGIC` | 服务端逻辑线程运行 |
| `NETWORK` | 网络线程运行 |

---

## 代码示例

### 定义 Payload

```java
// 1. 创建自定义 Payload
public class ExamplePayload implements 
        CustomPacketPayload {
    
    public static final PayloadType<ExamplePayload> TYPE = 
        PayloadType.create(
            ResourceLocation.fromNamespaceAndPath(
                MOD_ID, "example"),
            ExamplePayload::new
        );
    
    private final int value;
    private final Component message;
    
    public ExamplePayload(int value, Component message) {
        this.value = value;
        this.message = message;
        TYPE.executor().execute(this::handle);
    }
    
    private ExamplePayload(FriendlyByteBuf buf) {
        this.value = buf.readInt();
        this.message = buf.readComponent();
    }
    
    @Override
    public Id<?> id() {
        return TYPE.id();
    }
    
    @Override
    public void write(FriendlyByteBuf buf) {
        buf.writeInt(value);
        buf.writeComponent(message);
    }
    
    private void handle(ExamplePayload data) {
        // 处理接收到的数据
    }
}
```

### 注册 Payload

```java
// 1. 创建注册器
public static final NetworkConstants INSTANCE = 
    new NetworkConstants();

public class NetworkConstants {
    public final PayloadRegistrar registrar = 
        new PayloadRegistrar(INSTANCE.protocolVersion());
    
    private NetworkConstants() {
        register();
    }
    
    private void register() {
        registrar.play(
            ExamplePayload.TYPE.id(),
            // 服务端 -> 客户端
            ExamplePayload::new,
            (payload, context) -> {
                context.setPacketHandled(true);
                // 处理
            }
        );
        
        registrar.playToServer(
            ServerboundExamplePayload.TYPE.id(),
            ServerboundExamplePayload::new,
            (payload, context) -> {
                context.setPacketHandled(true);
                ServerPlayer player = context.getPlayer();
                // 处理来自客户端的数据
            }
        );
        
        registrar.playToClient(
            ClientboundExamplePayload.TYPE.id(),
            ClientboundExamplePayload::new,
            (payload, context) -> {
                context.setPacketHandled(true);
                // 处理来自服务端的数据
            }
        );
    }
}

// 2. 初始化网络
@Mod.EventBusSubscriber(modid = MOD_ID, 
    bus = Mod.EventBusSubscriber.Bus.MOD)
public static class NetworkInit {
    @SubscribeEvent
    public static void onInit(NetworkRegistryEvent.Init event) {
        // 使用 NeoForge.EVENT_BUS
    }
    
    @SubscribeEvent
    public static void registerPlayHandlers(
            RegisterPayloadHandlerEvent event) {
        event.registrar(MOD_ID)
            .play(
                ExamplePayload.TYPE.id(),
                ExamplePayload::new,
                payload -> payload.handle(null)
            );
    }
}
```

### 发送 Payload

```java
// 1. 服务端 -> 所有客户端
public static void broadcastToAll(
        ServerLevel level, 
        CustomPacketPayload payload) {
    ServerGamePacketListenerImpl connection = 
        level.getServer().getConnection();
    
    if (connection != null) {
        connection.broadcast(payload, 
            PacketDistributor.all());
    }
}

// 2. 服务端 -> 特定玩家
public static void sendTo(
        ServerPlayer player, 
        CustomPacketPayload payload) {
    player.connection.send(payload);
}

// 3. 服务端 -> 追踪实体的玩家
public static void sendToTracking(
        Entity entity, 
        CustomPacketPayload payload) {
    entity.serverLevel().getChunkSource()
        .broadcast(entity, payload);
}

// 4. 客户端 -> 服务端
public static void sendToServer(
        CustomPacketPayload payload) {
    Minecraft.getInstance().getConnection()
        .send(payload);
}

// 5. 使用 PacketDistributor
public static void sendToNear(
        ServerLevel level, 
        Vec3 position,
        double range,
        CustomPacketPayload payload) {
    PacketDistributor.Target target = 
        PacketDistributor.NEAR.with(
            PacketDistributor.TargetPoint.packet(
                position.x, position.y, position.z,
                range,
                level.dimension()
            )
        );
    level.getServer().getConnection()
        .broadcast(payload, target);
}
```

### 复杂 Payload

```java
// 1. 使用 Record（推荐）
public record EntitySpawnPayload(
    EntityType<?> type,
    int entityId,
    UUID uuid,
    double x, double y, double z,
    float yRot, float xRot
) implements CustomPacketPayload {
    
    public static final PayloadType<EntitySpawnPayload> TYPE = 
        PayloadType.create(
            ResourceLocation.fromNamespaceAndPath(
                MOD_ID, "entity_spawn"),
            EntitySpawnPayload::new
        );
    
    public EntitySpawnPayload(FriendlyByteBuf buf) {
        this(
            BuiltInRegistries.ENTITY_TYPE.byId(buf.readInt()),
            buf.readInt(),
            buf.readUUID(),
            buf.readDouble(),
            buf.readDouble(),
            buf.readDouble(),
            buf.readFloat(),
            buf.readFloat()
        );
    }
    
    @Override
    public Id<CustomPacketPayload> id() {
        return TYPE.id();
    }
    
    @Override
    public void write(FriendlyByteBuf buf) {
        buf.writeInt(BuiltInRegistries.ENTITY_TYPE
            .getId(type()));
        buf.writeInt(entityId());
        buf.writeUUID(uuid());
        buf.writeDouble(x());
        buf.writeDouble(y());
        buf.writeDouble(z());
        buf.writeFloat(yRot());
        buf.writeFloat(xRot());
    }
}

// 2. 使用 Codec
public record ComplexPayload(
    int intValue,
    String stringValue,
    List<ItemStack> items,
    Optional<Component> component
) implements CustomPacketPayload {
    
    public static final PayloadType<ComplexPayload> TYPE = 
        PayloadType.create(
            ResourceLocation.fromNamespaceAndPath(
                MOD_ID, "complex"),
            ComplexPayload::new
        );
    
    public static final Codec<ComplexPayload> CODEC = RecordCodecBuilder.create(
        instance -> instance.group(
            Codec.INT.fieldOf("intValue")
                .forGetter(ComplexPayload::intValue),
            Codec.STRING.fieldOf("stringValue")
                .forGetter(ComplexPayload::stringValue),
            Codec.list(EXTRA_CODEC)
                .fieldOf("items")
                .forGetter(ComplexPayload::items),
            ComponentCodec.CODEC.optionalFieldOf("component")
                .forGetter(ComplexPayload::component)
        ).apply(instance, ComplexPayload::new)
    );
    
    public ComplexPayload(FriendlyByteBuf buf) {
        this(
            buf.readInt(),
            buf.readUtf(),
            buf.readCollection(
                java.util.ArrayList::new, 
                ItemStack.OPTIONAL_SMALL_NBT
            ),
            buf.readOptional(
                FriendlyByteBuf::readComponent
            )
        );
    }
    
    @Override
    public Id<CustomPacketPayload> id() {
        return TYPE.id();
    }
    
    @Override
    public void write(FriendlyByteBuf buf) {
        buf.writeInt(intValue());
        buf.writeUtf(stringValue());
        buf.writeCollection(items(), 
            (b, s) -> s.writeOptional(
                b, ItemStack.OPTIONAL_SMALL_NBT)
        );
        buf.writeOptional(component(), 
            FriendlyByteBuf::writeComponent
        );
    }
}
```

---

## 注意事项

### 线程安全
- Payload 在网络线程接收
- 使用 `play` 注册的处理器在主线程执行
- 避免在 Payload 中进行阻塞操作

### 常见错误
1. **Payload 不被识别**：确认类型已正确注册
2. **序列化异常**：检查 `read`/`write` 方法对称性
3. **线程错误**：确认在正确线程执行操作

### 最佳实践

```java
// 推荐：使用 Record
public record MyPayload(int value) implements CustomPacketPayload {
    public static final PayloadType<MyPayload> TYPE = 
        PayloadType.create(
            ResourceLocation.fromNamespaceAndPath(MOD_ID, "my"),
            MyPayload::new
        );
    
    public MyPayload(FriendlyByteBuf buf) {
        this(buf.readInt());
    }
    
    @Override
    public Id<CustomPacketPayload> id() {
        return TYPE.id();
    }
    
    @Override
    public void write(FriendlyByteBuf buf) {
        buf.writeInt(value);
    }
}
```

---

## 关联引用

- 流编解码器：[NeoForge-网络-StreamCodec](./NeoForge-网络-StreamCodec.md)
- 网络基础：[NeoForge-网络基础](./NeoForge-网络基础.md)
