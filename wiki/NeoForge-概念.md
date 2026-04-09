# NeoForge 核心概念

## 注册表 (Registries)

### 概述
注册表是 Map<ID, Object> 的包装器，将注册名（`Identifier`）映射到注册对象。注册名格式：`namespace:path`（如 `minecraft:dirt`）。

### 核心类

| 类 | 说明 |
|-----|------|
| `DeferredRegister<T>` | 推荐使用的延迟注册工具 |
| `DeferredHolder<R, T>` | 注册持有者，持有注册对象 |
| `RegisterEvent` | 注册事件（底层机制） |
| `BuiltInRegistries` | Minecraft 内置注册表 |
| `NeoForgeRegistries` | NeoForge 注册表 |

### DeferredRegister 用法

```java
// 创建 DeferredRegister
public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(
    BuiltInRegistries.BLOCKS,  // 注册表
    MOD_ID                     // mod id
);

// 注册方块
public static final DeferredHolder<Block, Block> EXAMPLE_BLOCK = BLOCKS.register(
    "example_block",           // 注册名
    () -> new Block(...)       // 工厂Supplier
);

// 获取注册对象
Block block = EXAMPLE_BLOCK.get();
```

### DeferredRegister 快捷方式

```java
// 方块
DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(MOD_ID);

// 物品
DeferredRegister.Items ITEMS = DeferredRegister.createItems(MOD_ID);

// 实体
DeferredRegister.Entities ENTITIES = DeferredRegister.createEntities(MOD_ID);
```

### RegisterEvent 方式

```java
@SubscribeEvent  // mod event bus
public static void register(RegisterEvent event) {
    event.register(
        BuiltInRegistries.BLOCKS,
        registry -> {
            registry.register(
                Identifier.fromNamespaceAndPath(MOD_ID, "block"),
                new Block(...)
            );
        }
    );
}
```

### 查询注册表

```java
// 通过 ID 获取对象
BuiltInRegistries.BLOCKS.getValue(
    Identifier.fromNamespaceAndPath("minecraft", "dirt")
);

// 通过对象获取 ID
BuiltInRegistries.BLOCKS.getKey(Blocks.DIRT);

// 检查是否存在
BuiltInRegistries.BLOCKS.containsKey(
    Identifier.fromNamespaceAndPath("create", "brass_ingot")
);

// 遍历
for (Identifier id : BuiltInRegistries.BLOCKS.keySet()) { }
```

⚠️ **警告**: 注册期间禁止查询注册表！

---

## 自定义注册表

### 普通自定义注册表

```java
// 1. 创建注册表键
public static final ResourceKey<Registry<Spell>> SPELL_REGISTRY_KEY = 
    ResourceKey.createRegistryKey(
        Identifier.fromNamespaceAndPath(MOD_ID, "spells")
    );

// 2. 创建注册表
public static final Registry<Spell> SPELL_REGISTRY = 
    new RegistryBuilder<>(SPELL_REGISTRY_KEY)
        .sync(true)                                    // 网络同步
        .defaultKey(Identifier.fromNamespaceAndPath(MOD_ID, "empty"))
        .create();

// 3. 在 NewRegistryEvent 中注册
@SubscribeEvent
public static void register(NewRegistryEvent event) {
    event.register(SPELL_REGISTRY);
}

// 4. 使用 DeferredRegister
public static final DeferredRegister<Spell> SPELLS = 
    DeferredRegister.create(SPELL_REGISTRY, MOD_ID);
```

### Datapack 注册表

```java
@SubscribeEvent
public static void register(DataPackRegistryEvent.NewRegistry event) {
    event.dataPackRegistry(
        SPELL_REGISTRY_KEY,
        Spell.CODEC,           // 编解码器
        Spell.CODEC,           // 网络编解码器（可null）
        builder -> builder.maxId(256)
    );
}
```

---

## 事件系统 (Events)

### 事件总线

| 总线 | 说明 |
|------|------|
| `NeoForge.EVENT_BUS` | 游戏主总线 |
| Mod Event Bus | Mod 生命周期事件 |

### 注册方式

#### 方式1: IEventBus#addListener
```java
public ExampleMod(IEventBus modBus) {
    NeoForge.EVENT_BUS.addListener(ExampleMod::onLivingJump);
}

private static void onLivingJump(LivingEvent.LivingJumpEvent event) {
    event.getEntity().heal(1);
}
```

#### 方式2: @SubscribeEvent
```java
public class EventHandler {
    @SubscribeEvent
    public void onLivingJump(LivingEvent.LivingJumpEvent event) {
        // 处理事件
    }
}

// 在构造函数中注册
NeoForge.EVENT_BUS.register(new EventHandler());
// 或静态注册
NeoForge.EVENT_BUS.register(EventHandler.class);
```

#### 方式3: @EventBusSubscriber
```java
@EventBusSubscriber(modid = "examplemod")
public class EventHandler {
    @SubscribeEvent
    public static void onLivingJump(LivingEvent.LivingJumpEvent event) {
        // 自动注册
    }
}
```

### 事件类型

#### 可取消事件 (ICancellableEvent)
```java
@SubscribeEvent
public void onEvent(CancellableEvent event) {
    event.setCanceled(true);
    if (event.isCanceled()) { }
}
```

#### TriState/Result 事件
```java
event.setCanRender(TriState.FALSE);     // 禁用/启用/默认
event.setResult(MobDespawnEvent.Result.DENY);  // 拒绝/允许
```

#### 优先级
```java
@SubscribeEvent(priority = EventPriority.HIGH)  // HIGHEST/HIGH/NORMAL/LOW/LOWEST
```

### 生命周期顺序

1. Mod 构造函数
2. @EventBusSubscriber 扫描
3. FMLConstructModEvent
4. 注册事件（NewRegistry → RegisterEvent）
5. FMLCommonSetupEvent
6. 分端设置（FMLClientSetupEvent / FMLDedicatedServerSetupEvent）
7. InterModComms
8. FMLLoadCompleteEvent

### 常用事件

| 事件 | 总线 | 说明 |
|------|------|------|
| `RegisterEvent` | Mod Bus | 注册对象 |
| `NewRegistryEvent` | Mod Bus | 创建自定义注册表 |
| `FMLCommonSetupEvent` | Mod Bus | 通用初始化 |
| `FMLClientSetupEvent` | Mod Bus | 客户端初始化 |
| `GatherDataEvent` | Mod Bus | 数据生成 |

---

## Sides（物理端与逻辑端）

### 概念

| 概念 | 说明 |
|------|------|
| **物理端 (Physical)** | 运行的程序类型（Client/Server JAR） |
| **逻辑端 (Logical)** | 代码运行的上下文（Server/Client） |

### 区分

```java
// 逻辑端检查（最常用）
if (level.isClientSide()) {
    // 客户端逻辑
} else {
    // 服务端逻辑
}

// 物理端检查
if (FMLEnvironment.getDist() == Dist.CLIENT) {
    // 物理客户端
}

// Dist 枚举
Dist.CLIENT           // 物理客户端
Dist.DEDICATED_SERVER // 专用服务器
```

### 分端注册

```java
// @Mod 分端
@Mod(value = "examplemod", dist = Dist.CLIENT)
public class ExampleModClient { }

// 或在代码中检查
if (FMLEnvironment.getDist() == Dist.CLIENT) {
    // 客户端代码
}
```

### 关键原则

⚠️ **必须使用数据包传输跨端数据！**

⚠️ **始终在专用服务器上测试！**

⚠️ **避免使用静态字段存储分端数据！**

---

## 关联文档
- [NeoForge-入门.md](./NeoForge-入门.md) - 环境配置与项目初始化
- [NeoForge-方块.md](./NeoForge-方块.md) - 方块开发
- [NeoForge-物品.md](./NeoForge-物品.md) - 物品开发
- [NeoForge-网络.md](./NeoForge-网络.md) - 网络通信
