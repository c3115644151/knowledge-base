# NeoForge 渲染 - 着色器

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/rendering/shaders

## 概述

着色器（Shaders）是用于在 Minecraft 中实现高级视觉效果的技术。NeoForge 提供了对着色器的扩展支持，允许 mod 开发者注册自定义着色器程序。

## ShaderInstance

`ShaderInstance` 是 Minecraft 中管理着色器的核心类。

### 核心方法

| 方法 | 说明 |
|------|------|
| `ShaderInstance(ResourceProvider, ResourceLocation, VertexFormat)` | 构造着色器实例 |
| `getUniform(String name)` | 获取 Uniform 变量 |
| `safeGetUniform(String name)` | 安全获取 Uniform |
| `setSampler(String name, Object value)` | 设置采样器 |
| `setDefaultUniforms(VertexFormat.Mode, Matrix4f, Matrix4f, Window)` | 设置默认 Uniform |
| `markDirty()` | 标记需要更新 |
| `apply()` | 应用着色器 |
| `close()` | 关闭着色器 |

### 内置 Uniform

| Uniform | 说明 |
|---------|------|
| `MODEL_VIEW_MATRIX` | 模型视图矩阵 |
| `PROJECTION_MATRIX` | 投影矩阵 |
| `TEXTURE_MATRIX` | 纹理矩阵 |
| `SCREEN_SIZE` | 屏幕尺寸 |
| `COLOR_MODULATOR` | 颜色调制器 |
| `LIGHT0_DIRECTION` | 光源0方向 |
| `LIGHT1_DIRECTION` | 光源1方向 |
| `GLINT_ALPHA` | 反光透明度 |
| `FOG_START` | 雾开始距离 |
| `LINE_WIDTH` | 线条宽度 |

## 创建自定义着色器

### 1. 创建着色器文件

着色器文件放在 `assets/<modid>/shaders/` 目录下：

**顶点着色器 (examplemod:shaders/post/my_shader.json):**
```json
{
    "vertex": "examplemod:shaders/post/example.vert",
    "fragment": "examplemod:shaders/post/example.frag",
    "attributes": [
        "Position",
        "UV0",
        "UV1",
        "UV2",
        "Color"
    ],
    "uniforms": [
        { "name": "ProjMat", "type": "matrix4x4", "values": [1.0, 0.0, 0.0, 0.0] },
        { "name": "OutSize", "type": "vector2", "values": [1.0, 1.0] }
    ]
}
```

### 2. GLSL 着色器代码

**顶点着色器 (example.vert):**
```glsl
#version 150

in vec3 Position;
in vec2 UV0;
out vec2 texCoord;

uniform mat4 ProjMat;

void main() {
    gl_Position = ProjMat * vec4(Position, 1.0);
    texCoord = UV0;
}
```

**片段着色器 (example.frag):**
```glsl
#version 150

in vec2 texCoord;
out vec4 fragColor;

uniform sampler2D DiffuseSampler;
uniform vec2 OutSize;

void main() {
    fragColor = texture(DiffuseSampler, texCoord);
}
```

## 注册着色器

### 使用 ResourceProvider

```java
// 在客户端初始化期间
public class ModShaders {
    public static ShaderInstance createShader(ResourceProvider provider, String name) 
            throws IOException {
        ResourceLocation location = new ResourceLocation(ExampleMod.MODID, name);
        return new ShaderInstance(provider, location, DefaultVertexFormat.POSITION_COLOR);
    }
}
```

### 使用 ShaderInstanceSupplier

```java
@SubscribeEvent
public static void registerShaders(RegisterShadersEvent event) {
    try {
        event.registerShader(
            new ResourceLocation(Examplemod.MOD_ID, "shaders/post/example.json"),
            shaderInstance -> { /* 初始化逻辑 */ }
        );
    } catch (IOException e) {
        ExampleMod.LOGGER.error("Failed to register shader", e);
    }
}
```

## RenderPipeline

`RenderPipeline` 定义渲染对象的管线，包括着色器、格式、Uniform 等。

### 存储位置

通过 `GuiElementRenderState#pipeline` 存储。

### TextureSetup

定义用于渲染管线的采样器：
- `Sampler0`
- `Sampler1`
- `Sampler2`

通过 `GuiElementRenderState#textureSetup` 存储。

## 使用着色器的注意事项

### 1. 着色器文件格式

- Minecraft 1.14+ 使用 GLSL 1.50（#version 150）
- 文件必须是 `.glsl`、`.frag`、`.vert` 或 `.json` 格式

### 2. Uniform 同步

使用 `markDirty()` 标记 Uniform 需要更新，然后调用 `apply()` 应用。

### 3. 资源清理

使用完着色器后调用 `close()` 释放资源。

## 常用着色器类型

| 类型 | 用途 |
|------|------|
| `PositionColorTex` | 位置、颜色、纹理坐标 |
| `PositionTex` | 位置、纹理坐标 |
| `PositionColor` | 位置、颜色 |
| `Position` | 仅位置 |
| `NEW_ENTITY` | 实体渲染 |

## 第三方着色器 mod

### Iris

Iris 是流行的着色器 mod，支持 NeoForge 1.21+：
- 提供自定义着色器加载器
- 兼容 Sodium 等渲染优化 mod
- 支持大多数着色器包

安装方式：
1. 通过 Iris 原生安装程序
2. 通过 CurseForge/Modrinth 安装

## 关联引用

- [渲染特性](./NeoForge-渲染-特性.md)
- [纹理](./NeoForge-资源-纹理.md)
- [模型](./NeoForge-资源-模型.md)
