# NeoForge 实体渲染器

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/entities/renderer

## 概述

实体渲染器（Entity Renderer）用于定义实体的渲染行为，仅在物理和逻辑客户端存在。通过 `EntityRenderState` 管理渲染状态，使用 `RenderLayer` 添加渲染层。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `EntityRenderer<T>` | 实体渲染器基类 |
| `EntityRenderState` | 渲染状态 |
| `LivingEntityRenderer` | 生命实体渲染器 |
| `RenderLayer` | 渲染层 |
| `EntityModel<T>` | 实体模型 |
| `LayerDefinition` | 层定义 |

### 渲染器层级

```
EntityRenderer (抽象基类)
├── ArrowRenderer
├── AbstractBoatRenderer
├── AbstractMinecartRenderer
└── LivingEntityRenderer
    ├── ArmorStandRenderer
    ├── MobRenderer
    │   ├── AgeableMobRenderer
    │   │   └── HumanoidMobRenderer
    │   └── (其他怪物渲染器)
    └── PlayerRenderer
        └── AvatarRenderer
```

---

## 代码示例

### 创建基本渲染器

```java
// 1. 定义渲染状态
public class MyEntityRenderState extends EntityRenderState {
    public ItemStack heldItem;
    public float animationTime;
}

// 2. 创建渲染器
public class MyEntityRenderer extends EntityRenderer<MyEntity, 
        MyEntityRenderState> {
    
    private static final ResourceLocation TEXTURE = 
        ResourceLocation.fromNamespaceAndPath(
            MOD_ID, "textures/entity/my_entity.png");
    
    public MyEntityRenderer(EntityRendererProvider.Context context) {
        super(context);
    }
    
    @Override
    public MyEntityRenderState createRenderState() {
        return new MyEntityRenderState();
    }
    
    @Override
    public void extractRenderState(
            MyEntity entity, 
            MyEntityRenderState state, 
            float partialTick) {
        // 从实体提取数据到渲染状态
        state.heldItem = entity.getItemInHand(
            InteractionHand.MAIN_HAND);
        state.animationTime = entity.getViewYRot(partialTick);
    }
    
    @Override
    public void submit(
            MyEntityRenderState renderState,
            PoseStack poseStack,
            SubmitNodeCollector collector,
            CameraRenderState cameraState) {
        // 提交渲染指令
        super.submit(renderState, poseStack, 
            collector, cameraState);
        
        // 自定义渲染
        collector.submitModel(
            // ... 渲染逻辑
        );
    }
    
    @Override
    public ResourceLocation getTextureLocation(
            MyEntityRenderState state) {
        return TEXTURE;
    }
}

// 3. 注册渲染器
@Mod.EventBusSubscriber(modid = MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public static class RendererRegistration {
    @SubscribeEvent
    public static void registerRenderers(
            EntityRenderersEvent.RegisterRenderers event) {
        event.registerEntityRenderer(
            ModEntities.MY_ENTITY.get(),
            MyEntityRenderer::new
        );
    }
}
```

### 创建 LivingEntity 渲染器

```java
// 1. 定义模型层
public class MyEntityModel extends EntityModel<MyEntityRenderState> {
    private final ModelPart body;
    
    public MyEntityModel(ModelPart root) {
        super(root);
        this.body = root.getChild("body");
    }
    
    @Override
    public void setupAnim(
            MyEntityRenderState state) {
        // 设置模型动画
        this.body.xRot = state.rotationX;
        this.body.yRot = state.rotationY;
    }
    
    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        
        PartDefinition body = root.addOrReplaceChild(
            "body",
            CubeListBuilder.create()
                .texOffs(0, 0)
                .addBox(-4, -4, -4, 8, 8, 8),
            PartPose.offset(0, 8, 0)
        );
        
        return LayerDefinition.create(mesh, 64, 32);
    }
}

// 2. 定义模型层位置
public class MyEntityModel {
    public static final ModelLayerLocation LAYER = 
        new ModelLayerLocation(
            ResourceLocation.fromNamespaceAndPath(
                MOD_ID, "my_entity"),
            "main"
        );
}

// 3. 注册层定义
@Mod.EventBusSubscriber(modid = MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public static class LayerRegistration {
    @SubscribeEvent
    public static void registerLayers(
            EntityRenderersEvent.RegisterLayerDefinitions event) {
        event.register(MyEntityModel.LAYER, 
            MyEntityModel::createBodyLayer);
    }
}

// 4. 创建渲染器
public class MyLivingEntityRenderer extends 
        LivingEntityRenderer<MyEntity, 
            MyEntityRenderState, MyEntityModel> {
    
    public MyLivingEntityRenderer(
            EntityRendererProvider.Context context) {
        super(context,
            new MyEntityModel(
                context.bakeLayer(MyEntityModel.LAYER)),
            0.5f  // 阴影半径
        );
    }
    
    @Override
    public MyEntityRenderState createRenderState() {
        return new MyEntityRenderState();
    }
    
    @Override
    protected void scale(
            MyEntity entity,
            MyEntityRenderState state,
            PoseStack poseStack) {
        super.scale(entity, state, poseStack);
        // 自定义缩放
    }
}
```

### 自定义 RenderLayer

```java
// 1. 创建自定义层
public class MyRenderLayer extends RenderLayer<MyEntityRenderState, 
        MyEntityModel> {
    
    private final MyEntityModel model;
    
    public MyRenderLayer(
            MyEntityRenderer renderer,
            EntityModelSet modelSet) {
        super(renderer);
        this.model = new MyEntityModel(
            modelSet.bakeLayer(MyEntityModel.LAYER));
    }
    
    @Override
    public void submit(
            PoseStack poseStack,
            SubmitNodeCollector collector,
            int lightCoords,
            MyEntityRenderState renderState,
            float yRot,
            float xRot) {
        
        collector.submitModel(
            this.model,
            renderState,
            poseStack,
            lightCoords,
            OverlayTexture.DEFAULT_UV
        );
    }
}

// 2. 添加层到渲染器
public class MyLivingEntityRenderer extends 
        LivingEntityRenderer<MyEntity, 
            MyEntityRenderState, MyEntityModel> {
    
    public MyLivingEntityRenderer(
            EntityRendererProvider.Context context) {
        super(context,
            new MyEntityModel(
                context.bakeLayer(MyEntityModel.LAYER)),
            0.5f);
        
        // 添加自定义层
        this.addLayer(new MyRenderLayer(
            this, context.getModelSet()));
    }
}
```

### 修改现有渲染器

```java
@Mod.EventBusSubscriber(modid = MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public static class RendererModification {
    @SubscribeEvent
    public static void addLayers(
            EntityRenderersEvent.AddLayers event) {
        // 添加到所有实体
        for (EntityType<?> type : event.getEntityTypes()) {
            EntityRenderer<?, ?> renderer = 
                event.getRenderer(type);
            if (renderer instanceof MyCustomRenderer<?> custom) {
                custom.addLayer(new MyCustomLayer(custom, 
                    event.getEntityModels()));
            }
        }
    }
    
    @SubscribeEvent
    public static void addPlayerLayers(
            EntityRenderersEvent.AddLayers event) {
        // 为玩家模型添加
        for (PlayerModelType type : event.getSkins()) {
            AvatarRenderer<?> renderer = 
                event.getPlayerRenderer(type);
            if (renderer != null) {
                renderer.addLayer(new MyPlayerLayer(renderer,
                    event.getEntityModels()));
            }
        }
    }
}
```

### 使用 Blockbench 导出

```
Blockbench 导出设置：
1. 文件 -> 导出 -> 导出 Java 实体
2. 选择 "NeoForge" 格式
3. 复制生成的代码到模型类
4. 调整纹理路径
```

---

## 注意事项

### 性能考虑
- 避免在 `extractRenderState` 中进行复杂计算
- 使用 `RenderLayer` 分组渲染状态
- 合理的阴影半径影响性能

### 常见错误
1. **纹理未找到**：检查 `getTextureLocation` 返回值
2. **模型空指针**：确保层定义已注册
3. **动画异常**：`setupAnim` 中的旋转单位是弧度

### 最佳实践

```java
// 推荐：使用预计算的常量
private static final ResourceLocation TEXTURE = 
    ResourceLocation.fromNamespaceAndPath(MOD_ID, 
        "textures/entity/my_entity.png");

@Override
public ResourceLocation getTextureLocation(
        MyEntityRenderState state) {
    return TEXTURE;
}
```

---

## 关联引用

- 实体基础：[NeoForge-实体](./NeoForge-实体.md)
- 客户端资源：[NeoForge-客户端-模型](./NeoForge-客户端-模型.md)
- 渲染特性：[NeoForge-渲染-特性](./NeoForge-渲染-特性.md)
