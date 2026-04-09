# NeoForge-方块实体-渲染器

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/blockentities/ber

## 概述

BlockEntityRenderer（BER）用于以静态模型（JSON、OBJ 等）无法表示的方式"渲染"方块。例如，可以用来动态渲染箱子类方块的容器内容。BER 需要方块关联一个 BlockEntity，即使方块本身不存储任何数据。

## API 速查表

### 核心接口

| 接口/类 | 说明 |
|---------|------|
| `BlockEntityRenderer<T, S>` | 主渲染器接口 |
| `BlockEntityRenderState` | 渲染状态基类 |
| `BlockEntityRendererProvider.Context` | 渲染器上下文 |

### 注册事件

| 事件 | 说明 |
|------|------|
| `EntityRenderersEvent.RegisterRenderers` | 注册渲染器 |

## 代码示例

### 基本渲染器实现

```java
public class MyBlockEntityRenderer implements BlockEntityRenderer<MyBlockEntity, MyBlockEntityRenderState> {
    
    public MyBlockEntityRenderer(BlockEntityRendererProvider.Context context) {
        // 从 context 获取所需资源
    }

    @Override
    public MyBlockEntityRenderState createRenderState() {
        return new MyBlockEntityRenderState();
    }

    @Override
    public void extractRenderState(MyBlockEntity blockEntity, MyBlockEntityRenderState renderState, 
                                   float partialTick, Vec3 cameraPos, 
                                   @Nullable ModelFeatureRenderer.CrumblingOverlay crumblingOverlay) {
        // 必须调用 super
        super.extractRenderState(blockEntity, renderState, partialTick, cameraPos, crumblingOverlay);
        // 提取并存储渲染所需的值
        renderState.value = blockEntity.getValue();
    }

    @Override
    public void submit(MyBlockEntityRenderState renderState, PoseStack poseStack, 
                       SubmitNodeCollector collector, CameraRenderState cameraState) {
        // 通过 collector 提交渲染特征
    }
}
```

### 渲染状态

```java
public class MyBlockEntityRenderState extends BlockEntityRenderState {
    public boolean value;
    public int count;
    // 添加渲染所需的任何字段
}
```

### 注册渲染器

```java
@SubscribeEvent // 仅在物理客户端的 mod event bus 上
public static void registerEntityRenderers(EntityRenderersEvent.RegisterRenderers event) {
    event.registerBlockEntityRenderer(
        MyBlockEntities.MY_BLOCK_ENTITY.get(),  // BlockEntityType
        MyBlockEntityRenderer::new               // 构造函数引用
    );
}
```

### 简化版（无需 Context）

```java
public class MyBlockEntityRenderer implements BlockEntityRenderer<MyBlockEntity, MyBlockEntityRenderState> {
    // 不需要构造函数
}

// 注册时
event.registerBlockEntityRenderer(
    MyBlockEntities.MY_BLOCK_ENTITY.get(),
    context -> new MyBlockEntityRenderer()
);
```

## 物品方块渲染

对于无法用静态物品模型表示的方块实体，可以使用 `SpecialModelRenderer` 创建特殊渲染器。需要同时创建：
1. 特殊模型渲染器来提交渲染特征
2. 注册的特殊方块模型渲染器（用于方块被渲染而非物品的情况，如末影人搬运方块）

## 注意事项

1. **必须关联 BlockEntity**：BER 无法单独使用，必须有对应的 BlockEntity
2. **使用 RenderState**：从 BlockEntity 提取数据到 RenderState 进行渲染
3. **仅限客户端**：BER 只能在客户端物理端注册和使用
4. **提交特征**：通过 SubmitNodeCollector 提交渲染特征

## 关联引用

- [[NeoForge-方块实体]] - BlockEntity 基础
- [[NeoForge-资源-模型]] - 模型定义
- [[NeoForge-渲染-特性]] - 渲染特征系统
