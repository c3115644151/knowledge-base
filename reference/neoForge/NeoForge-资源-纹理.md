# NeoForge 资源 - 纹理

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/client/textures

## 概述

Minecraft 中所有纹理都是 PNG 文件，位于命名空间的 `textures` 文件夹内。JPG、GIF 和其他图片格式不受支持。

纹理路径相对于 `textures` 文件夹，例如 `examplemod:block/example_block` 指向 `assets/examplemod/textures/block/example_block.png`。

## 纹理尺寸

纹理通常应为 2 的幂次方大小，例如 16x16 或 32x32。与旧版本不同，现代 Minecraft 原生支持大于 16x16 的方块和物品纹理尺寸。

对于非 2 的幂次方大小的自定义渲染纹理（如 GUI 背景），创建下一个可用 2 的幂次方大小的空文件（通常 256x256），并将纹理放在该文件的左上角。

## 纹理元数据

纹理元数据可以在与纹理同名的文件中指定，加上 `.mcmeta` 后缀。例如 `textures/block/example.png` 需要附带 `textures/block/example.png.mcmeta` 文件。

### .mcmeta 格式

```json
{
    "texture": {
        "blur": true,
        "clamp": true,
        "mipmap_strategy": "mean",
        "alpha_cutoff_bias": 0.3
    },
    "gui": {
        "scaling": {
            "type": "stretch"
        },
        "scaling": {
            "type": "tile",
            "width": 16,
            "height": 16
        },
        "scaling": {
            "type": "nine_slice",
            "width": 16,
            "height": 16,
            "border": {
                "left": 0,
                "top": 0,
                "right": 0,
                "bottom": 0
            },
            "stretch_inner": true
        }
    },
    "animation": {}
}
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `texture.blur` | 纹理是否在需要时模糊，默认 false |
| `texture.clamp` | 纹理是否在需要时钳制，默认 false |
| `texture.mipmap_strategy` | Mipmap 生成策略：`mean`（默认）、`cutout`、`strict_cutout`、`dark_cutout` |
| `texture.alpha_cutoff_bias` | Mipmap 透明裁剪偏差 |
| `gui.scaling` | GUI 纹理缩放方式：`stretch`、`tile`、`nine_slice` |

### Mipmap 策略

- **mean**：默认，平均四个像素的颜色
- **cutout**：与 'mean' 类似，但使用原始纹理生成所有级别，alpha 值在 0.2 阈值处截断为 0 或 1
- **strict_cutout**：与 'cutout' 类似，但 alpha 截断阈值为 0.6
- **dark_cutout**：与 'mean' 类似，但仅当周围像素 alpha 不为 0 时才包含在平均中

## 动画纹理

Minecraft 原生支持方块和物品的动画纹理。动画纹理由不同动画阶段从上到下排列的纹理文件组成（例如，8 帧的 16x16 动画纹理表示为 16x128 PNG 文件）。

### animation 配置

```json
{
    "animation": {
        "frames": [1, 0],
        "frametime": 5,
        "interpolate": true,
        "width": 12,
        "height": 12
    }
}
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `frames` | 自定义帧播放顺序，省略则从上到下 |
| `frametime` | 帧切换间隔（以帧为单位），默认 1 |
| `interpolate` | 是否在动画阶段之间插值，默认 false |
| `width`/`height` | 单个动画阶段的宽度/高度，省略则使用纹理宽度 |

## 关联引用

- [模型](./NeoForge-资源-模型.md)
- [音效](./NeoForge-资源-音效.md)
- [粒子](../客户端/粒子.md)
