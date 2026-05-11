# Minecraft 机制：弹射物 (弹射物)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **实体注册 (Projectile Registration)**：在 NeoForge 中，弹射物（如自定义箭矢、投掷物）需要通过 `DeferredRegister<EntityType<?>>` 进行注册。弹射物类通常需要继承 `Projectile` 及其子类，例如 `AbstractArrow`（弓箭类）、`ThrowableItemProjectile`（雪球/末影珍珠类）。
- **客户端渲染绑定**：注册了弹射物实体后，**必须** 在客户端专用的事件总线（`EntityRenderersEvent.RegisterRenderers`）中为其分配一个 `EntityRenderer`，否则在游戏内抛出弹射物时会抛出空指针或渲染崩溃。原版提供了 `ThrownItemRenderer`（将物品直接渲染为投掷物）和 `ArrowRenderer`。
- **命中逻辑与同步**：弹射物最重要的逻辑是重写 `onHitEntity`（击中实体）和 `onHitBlock`（击中方块）。如果需要造成自定义的伤害，建议使用 `damageSources().thrown(this, this.getOwner())` 或自定义的伤害源，以保持原版的死亡信息结构。
- **自定义发射机制**：对于投掷物品（Item），通常在其 `use`（右键使用）方法中实例化你的 `Projectile` 类，并通过 `shootFromRotation` 方法设置其发射速度与散射度，随后调用 `level.addFreshEntity(projectile)` 生成。

---

## 极简代码示例 (Minimal Code Examples)

```java
// 1. 注册弹射物实体类型 (NeoForge)
public static final DeferredRegister<EntityType<?>> ENTITY_TYPES = DeferredRegister.create(Registries.ENTITY_TYPE, MOD_ID);

public static final DeferredHolder<EntityType<?>, EntityType<CustomProjectile>> CUSTOM_PROJECTILE = ENTITY_TYPES.register("custom_projectile", () ->
    EntityType.Builder.<CustomProjectile>of(CustomProjectile::new, MobCategory.MISC)
        .sized(0.25F, 0.25F)        // 碰撞箱尺寸
        .clientTrackingRange(4)     // 客户端追踪距离
        .updateInterval(10)         // 更新频率
        .build("custom_projectile") // Registry 名称
);

// 2. 弹射物实体类 (继承自 ThrowableItemProjectile)
public class CustomProjectile extends ThrowableItemProjectile {
    public CustomProjectile(EntityType<? extends CustomProjectile> type, Level level) {
        super(type, level);
    }
    
    // 自定义构造器：由玩家投掷时调用
    public CustomProjectile(Level level, LivingEntity shooter) {
        super(CUSTOM_PROJECTILE.get(), shooter, level);
    }

    @Override
    protected Item getDefaultItem() {
        return ModItems.CUSTOM_PROJECTILE_ITEM.get(); // 默认渲染的物品
    }

    // 重写命中实体时的逻辑
    @Override
    protected void onHitEntity(EntityHitResult result) {
        super.onHitEntity(result);
        if (!this.level().isClientSide()) {
            result.getEntity().hurt(this.damageSources().thrown(this, this.getOwner()), 5.0F);
        }
    }
}

// 3. 客户端注册渲染器 (Client Event Bus)
@SubscribeEvent
public static void registerEntityRenderers(EntityRenderersEvent.RegisterRenderers event) {
    // 借用原版的 ThrownItemRenderer，把投掷物渲染为 2D 物品形式
    event.registerEntityRenderer(CUSTOM_PROJECTILE.get(), ThrownItemRenderer::new);
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [生成](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#生成)
- [行为](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#行为)
  - [与实体碰撞](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#与实体碰撞)
  - [与方块碰撞](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#与方块碰撞)
  - [与世界边界碰撞](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#与世界边界碰撞)
- [弹射物分类](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#弹射物分类)
  - [箭类弹射物](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#箭类弹射物)
  - [火球类弹射物](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#火球类弹射物)
  - [物品弹射物](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#物品弹射物)
  - [投掷物](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#投掷物)
- [弹射物列表](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#弹射物列表)
- [实体数据](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#实体数据)
- [成就](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#成就)
- [进度](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#进度)
- [参考](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#参考)
- [导航](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#导航)
  - [个人工具](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
