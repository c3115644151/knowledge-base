# NeoForge 资源 - 模型

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/client/models/

## 概述

模型是确定方块或物品视觉形状和纹理的 JSON 文件。模型由立方体元素组成，每个元素有自己的尺寸，然后为每个面分配纹理。

物品使用其关联的[客户端物品模型](./物品.md)；方块使用[方块状态文件](#方块状态文件)中的关联模型。

## 模型规范

### 根属性

| 属性 | 说明 |
|------|------|
| `loader` | NeoForge 添加，设置自定义模型加载器 |
| `parent` | 父模型路径，常用父模型包括 `minecraft:block/block`、`minecraft:item/generated` |
| `ambientocclusion` | 是否启用环境光遮蔽，仅对方块模型有效，默认 true |
| `render_type` | NeoForge 添加，设置渲染类型组 |
| `gui_light` | `"front"` 或 `"side"`，仅对物品模型有效 |
| `textures` | 纹理变量到纹理位置的映射 |
| `elements` | 立方体元素列表 |
| `display` | 不同视角的显示选项 |
| `transform` | 根变换 |

### 常用父模型

| 父模型 | 用途 |
|--------|------|
| `minecraft:block/block` | 所有方块模型的通用父模型 |
| `minecraft:block/cube` | 使用 1x1x1 立方体模型的变体 |
| `minecraft:block/cube_all` | 所有六面使用相同纹理，如圆石或木板 |
| `minecraft:block/cube_bottom_top` | 四水平面相同，顶底分开的变体 |
| `minecraft:block/cube_column` | 有侧面纹理和底顶纹理，如木原木 |
| `minecraft:block/cross` | X 形状的两平面模型，用于植物 |
| `minecraft:item/generated` | 经典 2D 平面物品模型 |
| `minecraft:item/handheld` | 玩家实际持有的 2D 平面物品模型，用于工具 |

### 渲染类型组

使用 `render_type` 字段设置 `RenderTypeGroup`：

| 渲染类型 | 用途 |
|----------|------|
| `minecraft:solid` | 完全实心的模型，如石头 |
| `minecraft:cutout` | 像素完全实体或完全透明的模型，如玻璃 |
| `minecraft:translucent` | 像素可能半透明的模型，如染色玻璃 |
| `minecraft:tripwire` | 需要渲染到天气目标的特殊模型 |
| `neoforge:item_unlit` | NeoForge 添加，物品渲染时不考虑光照方向 |

## 元素（Elements）

元素是立方体对象的 JSON 表示：

```json
{
    "from": [0, 0, 0],
    "to": [16, 16, 16],
    "faces": {
        "north": { "uv": [0, 0, 16, 16], "texture": "#wood" },
        "south": { "uv": [0, 0, 16, 16], "texture": "#wood" },
        "east": { "uv": [0, 0, 16, 16], "texture": "#wood" },
        "west": { "uv": [0, 0, 16, 16], "texture": "#wood" },
        "up": { "uv": [0, 0, 16, 16], "texture": "#top" },
        "down": { "uv": [0, 0, 16, 16], "texture": "#bottom" }
    }
}
```

### 元素属性

| 属性 | 说明 |
|------|------|
| `from` | 起始角坐标，1/16 方块单位 |
| `to` | 结束角坐标，1/16 方块单位 |
| `faces` | 最多 6 个面的数据（north, south, east, west, up, down） |
| `shade` | 是否使用方向相关阴影，默认 true |
| `rotation` | 对象旋转 |

### 面属性

| 属性 | 说明 |
|------|------|
| `uv` | UV 坐标 `[u1, v1, u2, v2]` |
| `texture` | 纹理变量，以 `#` 开头 |
| `rotation` | 顺时针旋转 90、180 或 270 度 |
| `cullface` | 渲染引擎跳过渲染相邻完整方块的方向 |
| `tintindex` | 染色索引，用于染色处理器 |
| `neoforge_data` | 额外面数据（颜色、方块光、天光、环境光遮蔽） |

### 额外面数据（neoforge_data）

```json
{
    "neoforge_data": {
        "color": "0xFFFFFFFF",
        "block_light": 0,
        "sky_light": 0,
        "ambient_occlusion": true
    }
}
```

## 方块状态文件

每个注册的方块必须有一个方块状态文件。指定方块模型有三种互斥方式：

### variants

```json
{
    "variants": {
        "": { "model": "examplemod:block/example" },
        "facing=north": { "model": "examplemod:block/example", "y": 180 },
        "facing=south": { "model": "examplemod:block/example" }
    }
}
```

### multipart

```json
{
    "multipart": [
        { "when": { "OR": [{ "north": "true" }, { "south": "true" }] }, "apply": { "model": "examplemod:block/fence_post" } },
        { "when": { "north": "true" }, "apply": { "model": "examplemod:block/fence_side", "y": 90 } }
    ]
}
```

## 染色（Tinting）

某些方块根据位置和/或属性改变纹理颜色。通过事件注册染色处理器：

```java
@SubscribeEvent
public static void registerBlockColorHandlers(RegisterColorHandlersEvent.Block event) {
    event.register((state, level, pos, tintIndex) -> {
        return 0xFFFFFFFF; // ARGB 格式
    }, EXAMPLE_BLOCK.get());
}

@SubscribeEvent
public static void registerColorResolvers(RegisterColorHandlersEvent.ColorResolvers event) {
    event.register((biome, x, z) -> {
        return 0xFFFFFFFF;
    });
}
```

## 注册独立模型

通过 `ModelEvent.RegisterStandalone` 注册不与方块或物品关联的模型：

```java
public static final StandaloneModelKey<QuadCollection> EXAMPLE_KEY = new StandaloneModelKey<>(
    (ModelDebugName) () -> "examplemod: Example Model"
);

@SubscribeEvent
public static void registerAdditional(ModelEvent.RegisterStandalone event) {
    event.register(
        EXAMPLE_KEY,
        SimpleUnbakedStandaloneModel.quadCollection(
            Identifier.fromNamespaceAndPath("examplemod", "block/example_unused_model")
        )
    );
}
```

### 物品模型与 ClientItem（重要：1.21.x 双层结构）

> **⚠️ 1.21.x 物品模型必须同时配置两层**：
> 1. `models/item/<name>.json` — ItemModel（几何 + 纹理）
> 2. `assets/<modid>/items/<name>.json` — ClientItem（渲染配置，引用 ItemModel）

仅配置 `models/item/` 不足以让游戏找到物品模型！参考 [Client Items 官方文档](https://docs.neoforged.net/docs/resources/client/models/items)。

#### models/item/（ItemModel）

定义物品的几何形状和纹理：
```json
// assets/examplemod/models/item/example_item.json
{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "examplemod:item/example_item"
  }
}
```

#### items/（ClientItem）

渲染配置，引用上面的 ItemModel：
```json
// assets/examplemod/items/example_item.json
{
  "model": {
    "type": "minecraft:model",
    "model": "examplemod:item/example_item"
  }
}
```

Vanilla 可疑方块均有 `items/` ClientItem 文件（`suspicious_sand.json`、`suspicious_gravel.json` 等）。

## 关联引用

- [纹理](./NeoForge-资源-纹理.md)
- [音效](./NeoForge-资源-音效.md)
- [方块状态](./NeoForge-方块-状态.md)
