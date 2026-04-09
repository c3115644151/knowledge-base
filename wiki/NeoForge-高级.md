# NeoForge 高级主题

## 数据生成 (Datagen)

### GatherDataEvent

```java
@SubscribeEvent
public static void gatherData(GatherDataEvent.Client event) {
    // 注册数据生成器
    event.createProvider(output ->
        new MyRecipeProvider(output, event.getLookupProvider())
    );
    
    // 注册标签生成器
    event.createBlockAndItemTags(
        Registries.BLOCK,
        Registries.ITEM,
        MOD_ID,
        helper -> {
            // 添加标签内容
        }
    );
    
    // 注册数据包注册表对象
    event.createDatapackRegistryObjects(
        new RegistrySetBuilder()
            .add(Registries.CONFIGURED_FEATURE, bootstrap -> {
                // 注册世界生成特征
            }),
        Set.of(MOD_ID)
    );
}
```

### 配方生成器

```java
public class MyRecipeProvider extends RecipeProvider {
    public MyRecipeProvider(
            PackOutput output, 
            CompletableFuture<HolderLookup.Provider> registries) {
        super(output, registries);
    }
    
    @Override
    protected void buildRecipes(RecipeOutput output) {
        // 形状配方
        ShapedRecipeBuilder.shaped(output, Items.DIAMOND_SWORD, 1)
            .pattern(" X ")
            .pattern(" X ")
            .pattern(" # ")
            .define('X', Items.DIAMOND)
            .define('#', Items.STICK)
            .unlockedBy("has_diamond", has(Items.DIAMOND))
            .save(output);
        
        // 无序配方
        ShapelessRecipeBuilder.shapeless(output, Items.DIAMOND)
            .requires(Items.DIRT)
            .unlockedBy("has_dirt", has(Items.DIRT))
            .save(output);
    }
}
```

### 标签生成器

```java
// Block 和 Item 标签
event.createBlockAndItemTags(
    Registries.BLOCK,
    Registries.ITEM,
    MOD_ID,
    helper -> {
        // 标签内容
        helper.tag(Tags.Blockrs.MINEABLE_PICKAXE)
            .add(MyBlocks.MY_BLOCK.get());
    }
);

// 自定义标签
event.createProvider(output ->
    new TagsProvider<Block>(output, Registries.BLOCK, 
        PackOrigin.MOD, Set.of(MOD_ID)) {
        @Override
        protected void addTags(HolderLookup.Provider provider) {
            tag(Tags<Blockrs>.create(
                Identifier.fromNamespaceAndPath(MOD_ID, "my_tag")))
                .add(MyBlocks.MY_BLOCK.get());
        }
    }
);
```

### 战利品表生成

```java
public class MyLootProvider extends LootTableProvider {
    public MyLootProvider(PackOutput output, 
            CompletableFuture<HolderLookup.Provider> registries) {
        super(output, Set.of(), List.of(
            new LootTableSubprovider() {
                public void generate(HolderLookup.Provider registries, 
                        LootTableBuilder builder) {
                    builder.addBlock(
                        MyBlocks.MY_BLOCK.get(),
                        LootTable.lootTable()
                            .withPool(LootPool.lootPool()
                                .add(LootItem.lootItemItem(MyItems.MY_ITEM.get()))
                            )
                    );
                }
            }
        ));
    }
}
```

---

## 可扩展枚举 (Extensible Enums)

### 扩展 MobCategory

```java
// 1. 创建扩展值
public static final MobCategoryExtension EXTENDED_MOB = 
    new MobCategoryExtension("custom", 5, true, 128) {};

// 2. 注册
@SubscribeEvent
public static void register(
        RegistryEvent.Register<MobCategory> event) {
    EXTENDED_MOB.register();
}
```

### 扩展 SoundEvent

```java
// 1. 创建
public static final Holder<SoundEvent> MY_SOUND = 
    SoundEvent.registerVariable(
        Identifier.fromNamespaceAndPath(MOD_ID, "my_sound")
    );

// 2. 引用
SoundEvents.MY_SOUND  // 用作 SoundEvent
```

---

## 访问转换器 (Access Transformers)

### 配置

```toml
# neoforge.mods.toml
[[accessTransformers]]
file="at.cfg"
```

### at.cfg 示例

```
# public field
public-f net.minecraft.server.PlayerList field_12345 maxPlayers
# public method
public-f net.minecraft.world.entity.Entity *()
# private field
public net.minecraft.world.entity.Entity field_23456 speed
```

---

## Mixin 集成

### 配置

```toml
# neoforge.mods.toml
[[mixins]]
config="mymod.mixins.json"
```

### mixin.json

```json
{
    "required": true,
    "package": "com.example.mymod.mixin",
    "compatibilityLevel": "JAVA_21",
    "refmap": "mymod-common.refmap.json",
    "mixins": [
        "MixinExample"
    ],
    "client": [
        "MixinExampleClient"
    ],
    "injectors": {
        "defaultRequire": 1
    }
}
```

### Mixin 类

```java
@Mixin(Entity.class)
public abstract class MixinEntity {
    @Inject(
        at = @At("HEAD"),
        method = "tick()V"
    )
    private void onTick(CallbackInfo ci) {
        // 注入逻辑
    }
}
```

---

## 数据附件 (Data Attachments)

### 定义附件

```java
public static final ResourceKey<HolderLookup<DataComponentType<?>>> 
    MY_ATTACHMENT = ResourceKey.create(
        Registries.DATA_COMPONENT_TYPE,
        Identifier.fromNamespaceAndPath(MOD_ID, "my_attachment")
    );

public static final DataComponentType<MyData> MY_DATA = 
    DataComponentType.<MyData>builder()
        .persistent(MyData.CODEC)
        .networkSynchronized(MyData.STREAM_CODEC)
        .build();
```

### 使用附件

```java
// 获取
Optional<MyData> data = entity.getData(MY_ATTACHMENT);

// 设置
entity.setData(MY_ATTACHMENT, new MyData(value));

// 移除
entity.removeData(MY_ATTACHMENT);
```

---

## 配置系统

### 配置文件

```toml
# config/mymod.toml
[general]
enableFeature = true
count = 10

[server]
maxPlayers = 20
```

### 配置类

```java
public class MyConfig {
    public static final ForgeConfigSpec SPEC;
    
    public static final ConfigValue<Boolean> enableFeature;
    public static final ConfigValue<Integer> count;
    
    static {
        ForgeConfigSpec.Builder builder = new ForgeConfigSpec.Builder();
        
        builder.comment("General settings").push("general");
        enableFeature = builder.define("enableFeature", true);
        count = builder.defineInRange("count", 10, 1, 100);
        builder.pop();
        
        SPEC = builder.build();
    }
}
```

### 注册配置

```java
@Mod("mymodid")
public class MyMod {
    public MyMod(IEventBus modBus) {
        ModLoadingContext.get().registerConfig(
            Type.COMMON, 
            MyConfig.SPEC
        );
    }
}
```

---

## 游戏测试 (GameTest)

### 启用测试

```gradle
# build.gradle
minecraft {
    runs {
        gameTestServer {
            dataHolder = source(sourceSet.test)
        }
    }
}
```

### 测试结构

```java
public class MyGameTest {
    private static final String STRUCTURE = "mymod:my_test";
    
    @GameTestHolder
    public static void testExample(
            ExampleGameTestArgument testCase) {
        testCase.execute(level -> {
            BlockPos pos = testCase.origin().relative(
                testCase.direction(), 2);
            BlockState state = level.getBlockState(pos);
            Assertions.assertTrue(
                state.is(Blocks.DIAMOND_BLOCK),
                "Expected diamond block"
            );
        });
    }
}
```

### 常用断言

```java
Assertions.assertTrue(condition, "message");
Assertions.assertBlockPresent(Blocks.DIRT, pos);
Assertions.assertBlockNotPresent(Blocks.AIR, pos);
Assertions.assertItemsEqual(expected, actual);
```

---

## 性能优化

### 避免每 Tick 分配

```java
// 错误：每tick创建新对象
@Override
public void tick() {
    List<String> list = new ArrayList<>();
}

// 正确：预分配或使用对象池
private final List<String> cache = new ArrayList<>();
@Override
public void tick() {
    cache.clear();
}
```

### 批量操作

```java
// 批量发送数据包
List<CustomPacketPayload> packets = new ArrayList<>();
for (Entity entity : entities) {
    packets.add(new EntityDataPacket(entity));
}
PacketDistributor.sendToPlayersTrackingChunk(level, chunkPos, 
    new BatchedPacket(packets));
```

### 缓存查找结果

```java
// 使用缓存的 Holder
private final Holder<Block> cachedBlock = 
    BuiltInRegistries.BLOCK.getHolder(
        Identifier.fromNamespaceAndPath("minecraft", "diamond")
    ).orElseThrow();
```

---

## 调试技巧

### 调试日志

```java
private static final Logger LOGGER = 
    LoggerFactory.getLogger(MyMod.class);

// 使用标记
LOGGER.debug("Debug message {}", value);
LOGGER.info("Info message {}", value);
LOGGER.warn("Warning message {}", value);
LOGGER.error("Error message {}", value);
```

### 崩溃报告

```java
throw new IllegalStateException(
    "Expected condition not met", 
    new RuntimeException("Debug stack trace")
);
```

---

## 关联文档
- [NeoForge-入门.md](./NeoForge-入门.md) - 基础配置
- [NeoForge-资源.md](./NeoForge-资源.md) - 资源系统
- [NeoForge-网络.md](./NeoForge-网络.md) - 网络通信
