# Minecraft 世界生成：维度 (Dimension)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/维度](https://zh.minecraft.wiki/w/%E7%BB%B4%E5%BA%A6)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

在 1.21+ 中，自定义维度及其生成方式已完全被纳入**数据包 (Datapack)** 体系。硬编码维度已成为历史，开发者应使用 JSON 配合必要时的代码事件。

### NeoForge 对照文档

- [NeoForge 世界生成 - 维度（Dimensions）](../../neoForge/NeoForge-世界生成-维度.md)

### 1. 维度的双层注册架构
定义一个维度需要两个核心部分的 JSON 数据：
- **维度类型 (Dimension Type)** (`data/<namespace>/dimension_type/`)
  - 定义维度的**物理规则与逻辑属性**。
  - 核心字段：`ultrawarm` (水是否蒸发), `natural` (指南针/钟表是否正常工作), `has_ceiling` (是否有天花板), `piglin_safe` (猪灵是否会僵尸化), `bed_works` (是否能睡觉), `respawn_anchor_works` (重生锚是否可用), `min_y` 与 `height` (世界高度限制), `coordinate_scale` (坐标缩放比例，如原版下界的 0.125)。
- **维度实例 (Dimension)** (`data/<namespace>/dimension/`)
  - 将一个 `dimension_type` 绑定到一个**世界生成器 (Generator)** 上。
  - 生成器类型 (`type`)：
    - `minecraft:noise`: 最常用的地形生成器，通过柏林噪声生成高低起伏的地形。
    - `minecraft:flat`: 超平坦。
    - `minecraft:debug`: 调试世界。

### 2. 噪声生成器配置 (Noise Generator)
对于 `minecraft:noise` 生成器，需要配置两个主要属性：
- **biome_source** (生物群系来源)：
  - `minecraft:multi_noise`: 根据温度、湿度等参数动态分配生物群系（适用于主世界/下界风格）。
  - `minecraft:fixed`: 整个维度仅由单一生物群系构成（适用于末地风格或单一群系模组）。
  - `minecraft:checkerboard`: 棋盘状分布。
- **settings** (噪声设置)：
  - 指向 `worldgen/noise_settings` 注册表，定义具体的海平面高度、地形起伏曲线 (Density Functions)、以及地表材质覆盖规则 (Surface Rules)。

### 3. 维度传送机制 (Teleportation)
虽然维度本身是数据驱动的，但**传送门与传送逻辑**通常仍需要代码实现。
- **传送实体**：在 NeoForge 中，使用 `entity.changeDimension(ServerLevel destination, ITeleporter teleporter)` 进行维度切换。
- **自定义传送门**：
  - 需要实现 `ITeleporter` 接口，定义实体到达新维度时的坐标计算与生成逻辑（如放置传送门方块）。
  - 可以监听 `EntityTravelToDimensionEvent` 拦截或修改原版传送门行为。
- **自定义传送门方块**：通常创建一个类似原版下界传送门的方块，在实体碰撞 (`entityInside`) 时触发 `changeDimension`。

### 4. 常见开发坑点
- **世界保存与同步**：维度数据在世界创建时从数据包复制到 `level.dat` 中。如果在开发中途修改了维度的 JSON 定义，旧存档可能无法识别新配置，通常需要创建新世界测试。
- **客户端同步**：`dimension_type` 会同步给客户端（用于渲染雾气、天空等），但生成器信息仅保留在服务端。

---

## 极简代码示例 (Minimal Code Examples)

**数据包：自定义维度类型 (Dimension Type)**  
路径：`data/mymod/dimension_type/my_dim_type.json`
```json
{
  "ultrawarm": false,
  "natural": true,
  "coordinate_scale": 1.0,
  "has_skylight": true,
  "has_ceiling": false,
  "ambient_light": 0.0,
  "fixed_time": 6000,
  "monster_spawn_light_level": 0,
  "monster_spawn_block_light_limit": 0,
  "piglin_safe": false,
  "bed_works": true,
  "respawn_anchor_works": false,
  "has_raids": false,
  "logical_height": 256,
  "min_y": -64,
  "height": 384,
  "infiniburn": "#minecraft:infiniburn_overworld",
  "effects": "minecraft:overworld"
}
```

**代码：实体传送逻辑 (Entity Teleportation)**  
```java
// 在方块碰撞或交互事件中触发 (NeoForge 1.21+)
if (level instanceof ServerLevel serverLevel) {
    MinecraftServer server = serverLevel.getServer();
    ResourceKey<Level> destKey = ResourceKey.create(Registries.DIMENSION, ResourceLocation.fromNamespaceAndPath("mymod", "my_dim"));
    ServerLevel destLevel = server.getLevel(destKey);
    
    if (destLevel != null && !entity.level().dimension().equals(destKey)) {
        // 使用 1.21+ 引入的 DimensionTransition 配合 NeoForge ITeleporter
        DimensionTransition transition = new DimensionTransition(
            destLevel,
            entity.position(),
            entity.getDeltaMovement(),
            entity.getYRot(),
            entity.getXRot(),
            DimensionTransition.DO_NOTHING
        );
        entity.changeDimension(transition);
    }
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

### 1. 原版维度列表
- [主世界 (Overworld)](https://zh.minecraft.wiki/w/%E4%B8%BB%E4%B8%96%E7%95%8C) *(起始维度，Y范围 -64 到 320，标准气候)*
- [下界 (The Nether)](https://zh.minecraft.wiki/w/%E4%B8%8B%E7%95%8C) *(超高热、坐标比例 1:8、顶底基岩层)*
- [末地 (The End)](https://zh.minecraft.wiki/w/%E6%9C%AB%E5%9C%B0) *(虚空浮岛、无昼夜交替、固定生物群系源)*

### 2. 数据驱动与自定义维度
- [数据包：自定义维度](https://zh.minecraft.wiki/w/%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BB%B4%E5%BA%A6) *(Dimension JSON 结构详解，含 generator 配置)*
- [数据包：维度类型](https://zh.minecraft.wiki/w/%E7%BB%B4%E5%BA%A6%E7%B1%BB%E5%9E%8B) *(Dimension Type JSON 的环境光照、高度、物理逻辑配置)*

### 3. 实验性与愚人节维度
> *虽然不常用于常规开发，但这些页面展示了维度生成器的极限能力。*
- [20w14∞ (20亿个维度)](https://zh.minecraft.wiki/w/Java%E7%89%8820w14%E2%88%9E#%E4%B8%96%E7%95%8C%E7%94%9F%E6%88%90) *(基于字符串哈希的过程化维度生成展示)*
- [自定义世界 (Custom Worlds)](https://zh.minecraft.wiki/w/%E8%87%AA%E5%AE%9A%E4%B9%89) *(早期版本的世界定制机制历史)*

---

### Wiki 全目录（H2/H3/H4）

- [导航](https://zh.minecraft.wiki/w/%E7%BB%B4%E5%BA%A6#%E5%AF%BC%E8%88%AA)

## 相关资源与材质 (Assets)

- **实体传送**: `net.minecraft.world.entity.Entity#changeDimension`
- **传送器接口**: `net.neoforged.neoforge.common.util.ITeleporter`
- **自定义维度传送事件**: `net.neoforged.neoforge.event.entity.EntityTravelToDimensionEvent`
- **动态注册表访问**: `level.registryAccess().registryOrThrow(Registries.DIMENSION_TYPE)`
