# NeoForge-渲染-特性

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/rendering/feature

## 概述

渲染特性（Rendering Features）定义了不在关卡几何体中烘焙的对象集合，如实体、文本和粒子。这些对象通常有动态位置，因此 FallingBlock 和手持物品也属于此类别。特性渲染器的目的是更好地批处理和排序渲染到屏幕的对象。

## 提交特性

特性提交通常由负责这些对象的底层子系统处理：
- EntityRenderer 处理实体
- BlockEntityRenderer 处理方块实体
- 粒子渲染状态处理粒子

### SubmitNodeCollector 方法

| 方法 | 描述 |
|------|------|
| `submitShadow` | 指定半径、位置和透明度的黑色椭圆 |
| `submitNameTag` | 文本，透明度排序 |
| `submitText` | 文本 |
| `submitFlame` | 实体应用的火焰覆盖 |
| `submitLeash` | 24 段平面 |
| `submitModel` | 带渲染状态的模型，透明度排序 |
| `submitModelPart` | 模型部件 |
| `submitBlock` | 带烘焙光照的 BlockState |
| `submitMovingBlock` | 带动态光照的 BlockState |
| `submitBlockModel` | 带烘焙光照的 BlockStateModel |
| `submitItem` | 解构的 ItemStack 渲染状态 |
| `submitCustomGeometry` | 自定义几何体 |
| `submitParticleGroup` | 粒子批处理渲染器 |

## 渲染顺序

对于给定的 'order'，特性按以下顺序渲染：

1. 阴影
2. 不透明模型 → 排序透明模型
3. 模型部件
4. 实体火焰覆盖
5. 排序透明名称标签 → 不透明名称标签
6. 文本
7. 缰绳
8. 物品
9. 移动方块 → 方块 → 方块模型
10. 自定义几何体
11. 粒子

## 使用 SubmitNodeCollector

```java
// 在渲染器中
@Override
public void submit(MyRenderState renderState, PoseStack poseStack, 
                   SubmitNodeCollector collector, CameraRenderState cameraState) {
    // 提交模型
    collector.submitModel(model, renderState, poseStack);
    
    // 提交阴影
    collector.submitShadow(radius, x, y, z, opacity);
    
    // 提交文本
    collector.submitText(text, x, y, z, options);
    
    // 提交粒子组
    collector.order(1).submitParticleGroup(particleRenderer);
}
```

### 排序顺序

```java
// 默认 order 为 0
collector.submitModel(...);

// 在模型之前渲染
collector.order(-1).submitBlock(...);

// 在模型之后渲染
collector.order(1).submitParticleGroup(...);
```

## 注意事项

1. **提交后不可变**：元素提交后应视为不可变
2. **多次调用**：渲染器每帧可能调用多次
3. **批处理结束**：使用 `MultiBufferSource.BufferSource#endBatch` 结束批处理
4. **订单系统**：使用 `order()` 方法控制渲染顺序

## 关联引用

- [[NeoForge-方块实体-渲染器]] - BER 渲染
- [[NeoForge-实体-渲染器]] - 实体渲染
- [[NeoForge-渲染-着色器]] - 着色器
