# Minecraft：模型 (模型)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **DataGen (数据生成) 驱动**：在 NeoForge 1.21+ 开发中，极其不推荐手动编写模型 JSON。推荐继承 `BlockStateProvider` 和 `ItemModelProvider`，通过代码自动生成 `blockstates`、`models/block` 和 `models/item` 目录下的文件。
- **渲染类型 (Render Types) 声明**：自 1.20 起并延续至 1.21+，方块的透明/镂空渲染类型（如玻璃的半透明、草丛的镂空）**不再通过代码注册**，而是直接在方块模型 JSON 文件根级写入 `"render_type": "minecraft:translucent"` 或 `"minecraft:cutout"`。
- **自定义渲染逻辑**：
  - 若需要复杂动态渲染的方块实体，应编写 `BlockEntityRenderer` 并通过 `EntityRenderersEvent.RegisterRenderers` 注册。
  - 对于带有复杂模型的实体，需通过 `EntityRenderersEvent.RegisterLayerDefinitions` 注册模型定义（LayerDefinition），随后注册渲染器（EntityRenderer）。
- **物品内置模型重写**：1.21 中利用数据驱动的方式，可以通过覆盖原版或继承 `minecraft:item/generated` 来实现基于图层的标准 2D 物品渲染。对于 3D 物品，通常继承其方块模型。

---

## 极简代码示例 (Minimal Code Examples)

**1. 基础方块状态映射 (`assets/mymod/blockstates/my_block.json`)**
```json
{
  "variants": {
    "": { "model": "mymod:block/my_block" }
  }
}
```

**2. 基础方块模型（带渲染类型声明） (`assets/mymod/models/block/my_block.json`)**
```json
{
  "parent": "minecraft:block/cube_all",
  "render_type": "minecraft:cutout",
  "textures": {
    "all": "mymod:block/my_block_texture"
  }
}
```

**3. 基础物品模型 (`assets/mymod/models/item/my_item.json`)**
```json
{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "mymod:item/my_item_texture"
  }
}
```

**4. 注册方块实体渲染器 (BlockEntityRenderer)**
```java
@EventBusSubscriber(modid = "mymod", bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public class ClientModEvents {
    @SubscribeEvent
    public static void onRegisterRenderers(EntityRenderersEvent.RegisterRenderers event) {
        // 将自定义方块实体的渲染逻辑绑定到方块实体类型上
        event.registerBlockEntityRenderer(MY_BLOCK_ENTITY.get(), MyBlockEntityRenderer::new);
    }
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [模型分类](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#模型分类)
- [烘焙模型](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#烘焙模型)
  - [模型继承](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#模型继承)
  - [纹理变量](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#纹理变量)
  - [模型元素](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#模型元素)
  - [渲染变换](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#渲染变换)
  - [无效模型](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#无效模型)
- [方块模型](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#方块模型)
  - [方块状态映射](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#方块状态映射)
    - [直接指定方块状态](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#直接指定方块状态)
    - [多模型组合](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#多模型组合)
    - [候选模型](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#候选模型)
    - [物品展示框映射](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#物品展示框映射)
  - [模型面剔除](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#模型面剔除)
  - [方块粒子纹理变量](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#方块粒子纹理变量)
  - [方块着色](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#方块着色)
- [物品模型](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#物品模型)
  - [物品模型映射](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#物品模型映射)
  - [定义物品模型](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#定义物品模型)
    - [继承方块模型](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#继承方块模型)
    - [物品内置模型生成](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#物品内置模型生成)
  - [物品粒子纹理变量](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#物品粒子纹理变量)
- [动态模型](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#动态模型)
  - [动态模型结构](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#动态模型结构)
  - [动态模型的使用](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#动态模型的使用)
  - [动态模型纹理绑定](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#动态模型纹理绑定)
- [历史](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#历史)
  - [物品着色](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#物品着色)
- [参考](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#参考)
- [导航](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#导航)
  - [个人工具](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
