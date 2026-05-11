# Minecraft 机制：船 (船)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/%E8%88%B9](https://zh.minecraft.wiki/w/%E8%88%B9)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **船的类型 (Boat Types)**：原版中的船类型被硬编码在 `Boat.Type` 枚举中（如 OAK, SPRUCE, ACACIA 等）。在 NeoForge 中，若要给新添加的木材变种注册专属的船，建议不要直接修改枚举，而是去继承 `Boat`（或 `ChestBoat`），并通过独立的 EntityType 进行注册。这是一种更现代且能规避兼容性问题的方法。
- **自定义掉落物**：如果你扩展了原版的船实体类，最重要的就是覆盖 `getDropItem()` 方法，使其在受到破坏时掉落你自己注册的“船”物品（而不是原版的橡木船）。
- **客户端渲染与材质绑定**：在 1.21+ 中，如果你使用了自定义的船实体，那么还需要在 `EntityRenderersEvent.RegisterRenderers` 中注册客户端的 `BoatRenderer` 或其子类，从而将自己模组中指定位置的纹理（`.png` 贴图）覆盖到船的模型上。
- **运输和浮力物理**：原版船漂浮和与水流互动的物理引擎已经内建在 `Boat` 实体内部。绝大多数情况下，直接继承它就能直接享有原版的乘坐（Passenger）、浮沉以及摔落减伤特性。如果有特殊需求（比如岩浆船），则需要重写其环境判定的相关方法。

---

## 极简代码示例 (Minimal Code Examples)

```java
// 1. 注册自定义船实体
public static final DeferredRegister<EntityType<?>> ENTITY_TYPES = DeferredRegister.create(Registries.ENTITY_TYPE, MOD_ID);

public static final DeferredHolder<EntityType<?>, EntityType<CustomBoat>> CUSTOM_BOAT = ENTITY_TYPES.register("custom_boat", () ->
    EntityType.Builder.<CustomBoat>of(CustomBoat::new, MobCategory.MISC)
        .sized(1.375F, 0.5625F)  // 与原版船相同的尺寸
        .clientTrackingRange(10) // 追踪距离
        .build("custom_boat")
);

// 2. 自定义船实体类 (继承自 Boat)
public class CustomBoat extends Boat {
    public CustomBoat(EntityType<? extends Boat> type, Level level) {
        super(type, level);
    }

    // 由使用物品时触发实例化的构造器
    public CustomBoat(Level level, double x, double y, double z) {
        this(CUSTOM_BOAT.get(), level);
        this.setPos(x, y, z);
        this.xo = x;
        this.yo = y;
        this.zo = z;
    }

    // 覆盖掉落物为我们模组自己添加的船物品
    @Override
    public Item getDropItem() {
        return ModItems.CUSTOM_BOAT_ITEM.get();
    }
    
    // 注意：如果是实现箱子船，需继承 ChestBoat，
    // 并覆盖与容器相关的诸多方法。
}

// 3. 客户端渲染器注册 (NeoForge Client Event Bus)
public class CustomBoatRenderer extends BoatRenderer {
    // 绑定模组内部材质路径
    private final ResourceLocation texture = ResourceLocation.fromNamespaceAndPath(MOD_ID, "textures/entity/boat/custom_boat.png");

    public CustomBoatRenderer(EntityRendererProvider.Context context, boolean isChestBoat) {
        super(context, isChestBoat);
    }

    @Override
    public ResourceLocation getTextureLocation(Boat boat) {
        return texture; // 强制返回自定义材质
    }
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [物品列表](https://zh.minecraft.wiki/w/%E8%88%B9#物品列表)
- [获取](https://zh.minecraft.wiki/w/%E8%88%B9#获取)
  - [合成](https://zh.minecraft.wiki/w/%E8%88%B9#合成)
- [用途](https://zh.minecraft.wiki/w/%E8%88%B9#用途)
  - [合成材料](https://zh.minecraft.wiki/w/%E8%88%B9#合成材料)
  - [交易](https://zh.minecraft.wiki/w/%E8%88%B9#交易)
  - [燃料](https://zh.minecraft.wiki/w/%E8%88%B9#燃料)
- [行为](https://zh.minecraft.wiki/w/%E8%88%B9#行为)
  - [掉落](https://zh.minecraft.wiki/w/%E8%88%B9#掉落)
  - [控制](https://zh.minecraft.wiki/w/%E8%88%B9#控制)
  - [承载生物](https://zh.minecraft.wiki/w/%E8%88%B9#承载生物)
  - [摔落伤害](https://zh.minecraft.wiki/w/%E8%88%B9#摔落伤害)
  - [提供支撑](https://zh.minecraft.wiki/w/%E8%88%B9#提供支撑)
- [音效](https://zh.minecraft.wiki/w/%E8%88%B9#音效)
- [数据值](https://zh.minecraft.wiki/w/%E8%88%B9#数据值)
  - [ID](https://zh.minecraft.wiki/w/%E8%88%B9#ID)
  - [物品数据](https://zh.minecraft.wiki/w/%E8%88%B9#物品数据)
  - [实体数据](https://zh.minecraft.wiki/w/%E8%88%B9#实体数据)
- [成就](https://zh.minecraft.wiki/w/%E8%88%B9#成就)
- [进度](https://zh.minecraft.wiki/w/%E8%88%B9#进度)
- [历史](https://zh.minecraft.wiki/w/%E8%88%B9#历史)
- [你知道吗](https://zh.minecraft.wiki/w/%E8%88%B9#你知道吗)
- [画廊](https://zh.minecraft.wiki/w/%E8%88%B9#画廊)
- [参见](https://zh.minecraft.wiki/w/%E8%88%B9#参见)
- [参考](https://zh.minecraft.wiki/w/%E8%88%B9#参考)
- [导航](https://zh.minecraft.wiki/w/%E8%88%B9#导航)
  - [个人工具](https://zh.minecraft.wiki/w/%E8%88%B9#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/%E8%88%B9#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/%E8%88%B9#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/%E8%88%B9#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/%E8%88%B9#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/%E8%88%B9#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/%E8%88%B9#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E8%88%B9#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E8%88%B9#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E8%88%B9#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/%E8%88%B9#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/%E8%88%B9#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
