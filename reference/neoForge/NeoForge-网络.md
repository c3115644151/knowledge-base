# NeoForge 网络通信

## 概述

网络通信用于在服务端和客户端之间传递数据：
1. 同步服务端状态到客户端
2. 接收客户端操作请求

---

## Payload 系统

### 自定义 Payload

```java
public record MyData(String name, int value) implements CustomPacketPayload {
    // 1. 定义类型
    public static final CustomPacketPayload.Type<MyData> TYPE = 
        new CustomPacketPayload.Type<>(
            Identifier.fromNamespaceAndPath("mymodid", "my_data")
        );
    
    // 2. 定义 StreamCodec
    public static final StreamCodec<ByteBuf, MyData> STREAM_CODEC = 
        StreamCodec.composite(
            ByteBufCodecs.STRING_UTF8,
            MyData::name,
            ByteBufCodecs.VAR_INT,
            MyData::value,
            MyData::new
        );
    
    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
```

### StreamCodec 常用类型

| Codec | 说明 |
|-------|------|
| `ByteBufCodecs.BOOL` | 布尔值 |
| `ByteBufCodecs.BYTE` | 字节 |
| `ByteBufCodecs.INT` | 整数 |
| `ByteBufCodecs.VAR_INT` | 可变整数 |
| `ByteBufCodecs.LONG` | 长整数 |
| `ByteBufCodecs.VAR_LONG` | 可变长整数 |
| `ByteBufCodecs.FLOAT` | 浮点数 |
| `ByteBufCodecs.DOUBLE` | 双精度浮点数 |
| `ByteBufCodecs.STRING_UTF8` | UTF-8 字符串 |
| `ByteBufCodecs.ITEM_STACK` | ItemStack |
| `ByteBufCodecs.BlockPos` | 方块坐标 |
| `ByteBufCodecs.Vec3` | 三维向量 |
| `ByteBufCodecs.CompoundTag` | NBT 复合标签 |

### 复合 Codec

```java
// 多个字段
StreamCodec.composite(
    ByteBufCodecs.STRING_UTF8,  MyData::name,
    ByteBufCodecs.VAR_INT,      MyData::value,
    MyData::new
);

// 可选字段
StreamCodec.composite(
    ByteBufCodecs.STRING_UTF8, MyData::name,
    ByteBufCodecs.OPTIONAL_VARINT, MyData::optionalValue,
    MyData::new
);
```

---

## 注册 Payload

### 服务端注册

```java
@SubscribeEvent
public static void register(RegisterPayloadHandlersEvent event) {
    PayloadRegistrar registrar = event.registrar("1");
    
    // 双向（客户端<->服务端）
    registrar.playBidirectional(
        MyData.TYPE,
        MyData.STREAM_CODEC,
        ServerHandler::handle,
        ClientHandler::handle
    );
    
    // 仅发送到客户端
    registrar.playToServer(
        ServerData.TYPE,
        ServerData.STREAM_CODEC,
        ServerHandler::handle
    );
    
    // 仅发送到服务端
    registrar.playToClient(
        ClientData.TYPE,
        ClientData.STREAM_CODEC,
        ClientHandler::handle
    );
}
```

### 客户端注册（特殊情况）

```java
@SubscribeEvent
public static void register(RegisterClientPayloadHandlersEvent event) {
    // 客户端接收端需要单独注册
    event.register(
        MyData.TYPE,
        ClientHandler::handle
    );
}
```

### 线程配置

```java
PayloadRegistrar registrar = event.registrar("1")
    .executesOn(HandlerThread.NETWORK);  // 网络线程

// 或主线程（默认）
registrar.playBidirectional(..., HandlerThread.MAIN, ...);
```

---

## 消息处理器

### 服务端处理器

```java
public class ServerHandler {
    public static void handle(MyData data, IPayloadContext context) {
        // 获取发送者
        ServerPlayer player = (ServerPlayer) context.player();
        ServerLevel level = player.getLevel();
        
        // 主线程执行
        context.enqueueWork(() -> {
            // 服务端逻辑
            player.sendSystemMessage(
                Component.literal("Received: " + data.name())
            );
        });
    }
}
```

### 客户端处理器

```java
public class ClientHandler {
    public static void handle(MyData data, IPayloadContext context) {
        // 主线程执行
        context.enqueueWork(() -> {
            // 客户端逻辑（如更新 GUI）
            Minecraft mc = Minecraft.getInstance();
            if (mc.level != null) {
                // 更新 UI
            }
        });
    }
}
```

### 异常处理

```java
context.enqueueWork(() -> {
    // 业务逻辑
})
.exceptionally(e -> {
    // 处理异常
    context.disconnect(
        Component.translatable("mymod.network.error", e.getMessage())
    );
    return null;
});
```

---

## 发送 Payload

### 客户端发送到服务端

```java
// 在逻辑客户端
ClientPacketDistributor.sendToServer(new MyData("hello", 42));
```

### 服务端发送到客户端

```java
// 发送到单个玩家
PacketDistributor.sendToPlayer(player, new MyData("hello", 42));

// 发送到追踪 Chunk 的所有玩家
PacketDistributor.sendToPlayersTrackingChunk(level, chunkPos, new MyData(...));

// 发送到所有玩家
PacketDistributor.sendToAllPlayers(new MyData("broadcast", 0));

// 发送到附近玩家
PacketDistributor.sendToNear(level, pos, radius, new MyData(...));
```

### PacketDistributor 方法

| 方法 | 说明 |
|------|------|
| `sendToPlayer(player, payload)` | 发送到单个玩家 |
| `sendToPlayersTrackingChunk(level, chunkPos, payload)` | 发送到追踪 Chunk 的玩家 |
| `sendToAllPlayers(payload)` | 发送到所有玩家 |
| `sendToNear(level, pos, radius, payload)` | 发送到附近的玩家 |
| `sendToServer(payload)` | 客户端发送到服务端 |

---

## BlockEntity 同步

### 创建同步包

```java
public record BlockEntitySyncPacket(
        BlockPos pos, 
        int data
) implements CustomPacketPayload {
    
    public static final Type<BlockEntitySyncPacket> TYPE = 
        new Type<>(Identifier.fromNamespaceAndPath("mymodid", "be_sync"));
    
    public static final StreamCodec<ByteBuf, BlockEntitySyncPacket> CODEC =
        StreamCodec.composite(
            BlockPos.STREAM_CODEC,
            BlockEntitySyncPacket::pos,
            ByteBufCodecs.VAR_INT,
            BlockEntitySyncPacket::data,
            BlockEntitySyncPacket::new
        );
    
    @Override
    public Type<? extends CustomPacketPayload> type() { return TYPE; }
}
```

### 服务端发送

```java
// 在数据包处理器中
public static void handle(
        BlockEntitySyncRequest request, 
        IPayloadContext context) {
    context.enqueueWork(() -> {
        ServerPlayer player = (ServerPlayer) context.player();
        ServerLevel level = player.getLevel();
        
        BlockEntity be = level.getBlockEntity(request.pos());
        if (be instanceof MyBlockEntity myBE && level.hasChunkAt(request.pos())) {
            PacketDistributor.sendToPlayer(
                player,
                new BlockEntitySyncPacket(request.pos(), myBE.getData())
            );
        }
    });
}
```

### 客户端接收

```java
public static void handle(BlockEntitySyncPacket packet, IPayloadContext context) {
    context.enqueueWork(() -> {
        Minecraft mc = Minecraft.getInstance();
        if (mc.level == null) return;
        
        BlockEntity be = mc.level.getBlockEntity(packet.pos());
        if (be instanceof MyBlockEntity myBE) {
            myBE.setData(packet.data());
        }
    });
}
```

---

## 注意事项

### 大小限制
- **客户端→服务端**: < 32 KiB
- **服务端→客户端**: ≤ 1 MiB

### 线程安全
- 默认在主线程执行
- 可配置 `HandlerThread.NETWORK` 在网络线程执行
- 网络线程操作需使用 `enqueueWork` 提交到主线程

### 常见错误
- ❌ 在数据包中直接操作游戏对象
- ❌ 忘记检查 BlockEntity 是否存在
- ❌ 在 Chunk 未加载时同步
- ❌ 发送过大的数据包

### 安全检查
```java
if (level.hasChunkAt(pos)) {
    BlockEntity be = level.getBlockEntity(pos);
    if (be != null && !be.isRemoved()) {
        // 安全使用
    }
}
```

## 关联文档
- [NeoForge-方块实体.md](./NeoForge-方块实体.md) - BlockEntity 同步
- [NeoForge-概念.md](./NeoForge-概念.md) - Sides 概念
