# Minecraft 机制：矿车 (矿车)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **自定义矿车类型 (Custom Minecarts)**：在 1.21+ 中，如果你希望创建一个全新功能的矿车（例如动力矿车或带有特殊方块的矿车），最佳实践是继承 `AbstractMinecart` 并注册一个新的 `EntityType`。同时，需要通过覆盖 `getDropItem()` 确保矿车被摧毁时掉落正确的自定义矿车物品。
- **矿车行为覆盖 (Minecart overriding)**：NeoForge 提供了一套专门针对矿车扩展的机制。你可以通过覆盖 `AbstractMinecart` 中的一系列方法，比如 `getMaxSpeed()`，来改变矿车的最高速度（原版为 `0.4D`，即 `8 m/s`）。还可以利用类似 `IMinecartBehavior` 等接口来自定义特殊的行为。
- **自定义轨道的交互**：如果需要创建自定义轨道（如高速铁轨），往往需要在方块逻辑或实体层面上重写相关的交互行为。对于复杂的运动轨迹（如跨越方块碰撞箱），NeoForge 允许在实体层直接拦截移动逻辑进行重写。
- **实体状态数据同步**：如果你在矿车内嵌了一个容器（类似漏斗矿车、箱子矿车），你需要实现原版的容器和物品栏接口，并确保这些数据的客户端同步逻辑（Entity Data Parameters）是正确的。

---

## 极简代码示例 (Minimal Code Examples)

```java
// 1. 注册自定义矿车实体
public static final DeferredRegister<EntityType<?>> ENTITY_TYPES = DeferredRegister.create(Registries.ENTITY_TYPE, MOD_ID);

public static final DeferredHolder<EntityType<?>, EntityType<CustomMinecart>> CUSTOM_MINECART = ENTITY_TYPES.register("custom_minecart", () ->
    EntityType.Builder.<CustomMinecart>of(CustomMinecart::new, MobCategory.MISC)
        .sized(0.98F, 0.7F) // 原版矿车尺寸
        .clientTrackingRange(8)
        .build("custom_minecart")
);

// 2. 矿车覆盖逻辑 (Custom Minecart Class)
public class CustomMinecart extends AbstractMinecart {
    
    // 给实体注册表使用的构造函数
    public CustomMinecart(EntityType<?> type, Level level) {
        super(type, level);
    }

    // 物品放置时调用的构造函数
    public CustomMinecart(Level level, double x, double y, double z) {
        super(CUSTOM_MINECART.get(), level);
        this.setPos(x, y, z);
    }

    // 覆盖掉落物：确保被破坏后掉落正确的物品
    @Override
    protected Item getDropItem() {
        return ModItems.CUSTOM_MINECART_ITEM.get(); 
    }

    @Override
    public Type getMinecartType() {
        // 如果继承自原版的类型则返回对应的类型，或直接返回 RIDEABLE (可乘坐)
        return Type.RIDEABLE; 
    }
    
    // NeoForge 特有：覆盖最大速度逻辑 (Minecart overriding)
    @Override
    public double getMaxSpeed() {
        // 让这辆矿车的最高速度变成原版的两倍
        return super.getMaxSpeed() * 2.0D; 
    }
    
    // 自定义矿车与其他矿车相撞时的表现
    @Override
    public boolean isPushable() {
        return true;
    }
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [获取](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#获取)
  - [合成](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#合成)
  - [其他矿车](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#其他矿车)
- [用途](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#用途)
  - [合成材料](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#合成材料)
- [行为](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#行为)
  - [生物](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#生物)
    - [乘坐](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#乘坐)
    - [下车](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#下车)
  - [移动](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#移动)
    - [速度](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#速度)
    - [东南规则](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#东南规则)
    - [下坡定律](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#下坡定律)
    - [坡道排除/单向效应](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#坡道排除/单向效应)
    - [弯道交叉](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#弯道交叉)
    - [轨道性能](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#轨道性能)
  - [掉落](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#掉落)
  - [矿车重叠](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#矿车重叠)
  - [空矿车的倾斜和加速](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#空矿车的倾斜和加速)
  - [碰撞](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#碰撞)
  - [船](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#船)
  - [实验性](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#实验性)
- [音效](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#音效)
- [数据值](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#数据值)
  - [ID](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#ID)
  - [物品数据](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#物品数据)
  - [实体数据](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#实体数据)
- [成就](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#成就)
- [历史](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#历史)
- [你知道吗](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#你知道吗)
- [画廊](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#画廊)
- [注释](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#注释)
- [参考](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#参考)
- [导航](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#导航)
  - [个人工具](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
