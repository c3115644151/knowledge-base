# NeoForge-渲染-模型容器

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/rendering/initialization

## 概述

模型容器（Model Containers）是 NeoForge 提供的模型加载和渲染系统。它扩展了原版 Minecraft 的模型系统，允许开发者注册额外的模型和创建自定义模型加载器。

## 核心架构

### 模型加载管道

```
JSON 文件 → UnbakedModel → UnbakedGeometry → QuadCollection → BakedModel
```

| 阶段 | 类 | 描述 |
|------|-----|------|
| 解析 | `UnbakedModel` | 从 JSON 读取模型数据 |
| 几何体 | `UnbakedGeometry` | 定义模型的未烘焙几何数据 |
| 烘焙 | `QuadCollection` | 存储烘焙后的 BakedQuad |
| 渲染 | `BakedModel` | 最终用于渲染的模型 |

## API 速查表

### 模型事件 (ModelEvent)

| 事件 | 触发时机 | 用途 |
|------|----------|------|
| `ModelEvent.RegisterAdditional` | 模型加载前 | 注册独立模型 |
| `ModelEvent.RegisterLoaders` | 模型加载器注册时 | 注册自定义模型加载器 |
| `ModelEvent.ModifyBakingResult` | 模型烘焙完成后 | 修改烘焙结果 |
| `RegisterColorHandlersEvent` | 颜色处理器注册时 | 注册物品/方块颜色处理器 |

### 核心接口

| 接口 | 描述 |
|------|------|
| `UnbakedModelLoader<T>` | 模型加载器接口 |
| `ExtendedUnbakedGeometry` | 扩展未烘焙几何体 |
| `AbstractUnbakedModel` | 抽象未烘焙模型基类 |
| `IGeometryLoader<T>` | 几何体加载器 (旧 API) |

### 关键类

| 类 | 描述 |
|-----|------|
| `QuadCollection` | 存储烘焙后的四边形集合 |
| `QuadCollection.Builder` | 构建 QuadCollection |
| `TextureSlots` | 纹理槽位映射 |
| `ModelBaker` | 模型烘焙器 |
| `ModelState` | 模型状态 (UV 旋转等) |

## 注册额外模型

对于不与方块或物品关联但需要在其他上下文（如方块实体渲染器）使用的模型，通过 `ModelEvent.RegisterAdditional` 注册：

```java
@SubscribeEvent
public static void registerAdditional(ModelEvent.RegisterAdditional event) {
    // 注册独立方块模型
    event.register(ResourceLocation.fromNamespaceAndPath("examplemod", "block/standalone_model"));
    
    // 注册物品模型
    event.register(ModelResourceLocation.inventory(
        ResourceLocation.fromNamespaceAndPath("examplemod", "item/custom_item_model")
    ));
}
```

## 创建自定义模型加载器

### 完整流程

1. 创建 `UnbakedModelLoader` 类
2. 创建 `ExtendedUnbakedGeometry` 几何体类
3. 创建 `AbstractUnbakedModel` 模型类
4. 在事件中注册加载器

### 代码示例

```java
// 1. 模型加载器
public class MyUnbakedModelLoader implements UnbakedModelLoader<MyUnbakedModel>, 
                                              ResourceManagerReloadListener {
    public static final MyUnbakedModelLoader INSTANCE = new MyUnbakedModelLoader();
    public static final Identifier ID = Identifier.fromNamespaceAndPath("examplemod", "my_loader");
    
    private MyUnbakedModelLoader() {}
    
    @Override
    public MyUnbakedModel load(ResourceLocation id, JsonObject json, 
                                 JsonDeserializationContext context) {
        // 从 JSON 读取参数
        float scale = GsonHelper.getAsFloat(json, "scale", 1.0f);
        return new MyUnbakedModel(/* params */, new MyUnbakedGeometry(scale));
    }
    
    @Override
    public void onResourceManagerReload(ResourceManager resourceManager) {
        // 清理缓存
    }
}

// 2. 几何体类
public class MyUnbakedGeometry extends ExtendedUnbakedGeometry {
    private final float scale;
    
    public MyUnbakedGeometry(float scale) {
        this.scale = scale;
    }
    
    @Override
    public QuadCollection bake(TextureSlots textureSlots, ModelBaker baker, 
                                ModelState state, ModelDebugName debugName,
                                ContextMap additionalProperties) {
        var builder = new QuadCollection.Builder();
        
        // 创建自定义四边形
        builder.addUnculledFace(new BakedQuad(...));
        
        return builder.build();
    }
}

// 3. 模型类
public class MyUnbakedModel extends AbstractUnbakedModel {
    private final MyUnbakedGeometry geometry;
    
    public MyUnbakedModel(StandardModelParameters params, MyUnbakedGeometry geometry) {
        super(params);
        this.geometry = geometry;
    }
    
    @Override
    public UnbakedGeometry geometry() {
        return this.geometry;
    }
    
    @Override
    public void fillAdditionalProperties(ContextMap.Builder propertiesBuilder) {
        super.fillAdditionalProperties(propertiesBuilder);
        // 添加额外属性
    }
}

// 4. 注册
@SubscribeEvent
public static void registerLoaders(ModelEvent.RegisterLoaders event) {
    event.register(MyUnbakedModelLoader.ID, MyUnbakedModelLoader.INSTANCE);
}

// 5. 添加资源监听器（如果需要缓存）
@SubscribeEvent
public static void addClientResourceListeners(AddClientReloadListenersEvent event) {
    event.addListener(MyUnbakedModelLoader.ID, MyUnbakedModelLoader.INSTANCE);
    event.addDependency(MyUnbakedModelLoader.ID, VanillaClientListeners.MODELS);
}
```

### JSON 使用方式

```json
{
    "loader": "examplemod:my_loader",
    "scale": 2.0
}
```

## 内置模型加载器

### Composite Model (复合模型)

用于组合多个模型部件，可动态切换可见性：

```json
{
    "loader": "neoforge:composite",
    "children": {
        "part_1": {
            "parent": "examplemod:model_1"
        },
        "part_2": {
            "parent": "examplemod:model_2"
        }
    },
    "visibility": {
        "part_2": false
    }
}
```

继承时可覆盖可见性：

```json
{
    "parent": "examplemod:composite_parent",
    "visibility": {
        "part_1": false,
        "part_2": true
    }
}
```

### Fluid Container Model (流体容器模型)

```json
{
    "loader": "neoforge:fluid_container",
    "fluid": "examplemod:custom_fluid",
    "textures": {
        "base": "examplemod:item/container",
        "fluid": "examplemod:item/container_fluid"
    }
}
```

## 模型数据 (ModelData)

NeoForge 提供 `ModelData` 系统，用于从方块实体传递数据到模型：

```java
// 方块实体实现
public class MyBlockEntity extends BlockEntity implements IModelDataProvider {
    private final ModelData data = new ModelData();
    
    @Override
    public ModelData getModelData() {
        return data;
    }
    
    public void updateModelData(Property property, int value) {
        data.setData(property, value);
        requestModelDataUpdate();
    }
}

// 颜色处理器中使用
@SubscribeEvent
public static void registerBlockColorHandlers(RegisterColorHandlersEvent.Block event) {
    event.register((state, world, pos, tintIndex) -> {
        if (world != null && pos != null) {
            MyBlockEntity be = (MyBlockEntity) world.getBlockEntity(pos);
            return be.getModelData().getData(MyProperties.COLOR_PROPERTY);
        }
        return 0xFFFFFF;
    }, EXAMPLE_BLOCK.get());
}
```

## 注意事项

### 常见错误

1. **模型未注册**：独立模型必须通过 `RegisterAdditional` 事件注册
2. **纹理未找到**：确保纹理资源路径正确
3. **循环依赖**：避免模型间的循环引用
4. **缓存未清理**：实现 `ResourceManagerReloadListener` 时记得清理缓存

### 版本差异

- **NeoForge 26.x (1.21.11)**：使用新的 `UnbakedModelLoader` API
- **早期版本**：使用 `IGeometryLoader` 旧 API

### 性能优化

1. 复用烘焙后的 `QuadCollection`
2. 避免在 `bake()` 方法中执行耗时操作
3. 使用单例模式管理模型加载器

## 关联引用

- [[NeoForge-渲染-特性]] - 渲染特性与提交系统
- [[NeoForge-渲染-着色器]] - 自定义着色器
- [[NeoForge-方块实体-渲染器]] - 方块实体渲染
- [[NeoForge-资源-模型]] - 原版模型系统
- [[NeoForge-实体-渲染器]] - 实体渲染器
