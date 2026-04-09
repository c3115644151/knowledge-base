# NeoForge 渲染特性

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/rendering/feature

## 概述

渲染特性（Features）系统定义了不烘焙到关卡几何体中的对象集合，如实体、文本、粒子等。这些对象通常具有动态位置。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `SubmitNodeCollector` | 提交节点收集器 |
| `PoseStack` | 姿态堆栈 |
| `SubmitOrder` | 提交顺序 |

---

## 代码示例

### 提交渲染对象

```java
// 1. 提交模型
collector.submitModel(
    model,
    renderState,
    poseStack,
    lightCoords,
    OverlayTexture.DEFAULT_UV
);

// 2. 提交文本
collector.submitText(
    Component.literal("Hello"),
    1.0,  // x
    1.0,  // y
    0.0,  // z
    true, // 居中
    poseStack,
    MultiBufferSource.bufferSource(),
    lightCoords
);

// 3. 提交粒子组
collector.submitParticleGroup(
    particleType,
    poseStack,
    MultiBufferSource.bufferSource(),
    lightCoords
);

// 4. 提交阴影
collector.submitShadow(
    radius,
    x, y, z,
    opacity,
    poseStack
);

// 5. 控制渲染顺序
collector.order(1).submitModel(...);
```

### 渲染阶段

```
1. 阴影 (Shadows)
2. 不透明模型 -> 排序透明模型
3. 模型部件
4. 实体火焰覆盖
5. 排序透明名称标签 -> 不透明名称标签
6. 文本
7. 缰绳
8. 物品
9. 移动方块 -> 方块 -> 方块模型
10. 自定义几何体
11. 粒子
```

---

## 注意事项

### 性能考虑
- 合理使用 `order` 控制渲染顺序
- 避免提交过多对象
- 使用批处理优化粒子渲染

---

## 关联引用

- 实体渲染：[NeoForge-实体-渲染器](./NeoForge-实体-渲染器.md)
- 粒子系统：[NeoForge-客户端-粒子](./NeoForge-客户端-粒子.md)
