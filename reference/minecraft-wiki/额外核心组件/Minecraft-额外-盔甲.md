# Minecraft 机制：盔甲 (盔甲)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **组件化盔甲数据 (DataComponents.ARMOR)**：在 1.21+ 中，物品系统进行了重大重构。盔甲的防御值、韧性、击退抗性等核心属性不再直接依赖于 `ArmorItem` 的构造函数传递，而是通过数据组件 `DataComponents.ARMOR`（或对应的 NeoForge 等效组件）附加到物品上。
- **自定义盔甲材料 (`ArmorMaterial`)**：在 1.21 中，`ArmorMaterial` 已成为数据驱动或静态注册的 Record。可以通过 `DeferredRegister` 或数据包来定义新的盔甲材料，并通过 `ArmorItem.Type`（如 `HELMET`, `CHESTPLATE` 等）来确定每个部位的具体数值。
- **外观与纹理渲染**：渲染自定义盔甲模型和纹理，需要在 `ArmorMaterial.Layer` 中指定纹理路径（如 `ResourceLocation`），原版会自动拼接 `_layer_1.png` 和 `_layer_2.png`。如果需要完全自定义模型（如 3D 盔甲），则需要在客户端事件（如 `EntityRenderersEvent.AddLayers` 或 `RegisterClientExtensions`）中处理。

---

## 极简代码示例 (Minimal Code Examples)

```java
// 1. 注册自定义盔甲材料 (NeoForge 1.21+)
public static final DeferredRegister<ArmorMaterial> ARMOR_MATERIALS = DeferredRegister.create(Registries.ARMOR_MATERIAL, MOD_ID);

public static final DeferredHolder<ArmorMaterial, ArmorMaterial> CUSTOM_ARMOR = ARMOR_MATERIALS.register("custom", () -> 
    new ArmorMaterial(
        Util.make(new EnumMap<>(ArmorItem.Type.class), map -> {
            map.put(ArmorItem.Type.BOOTS, 2);
            map.put(ArmorItem.Type.LEGGINGS, 5);
            map.put(ArmorItem.Type.CHESTPLATE, 6);
            map.put(ArmorItem.Type.HELMET, 2);
        }),
        9, // 附魔等级 (Enchantment value)
        SoundEvents.ARMOR_EQUIP_IRON,
        () -> Ingredient.of(ModItems.CUSTOM_INGOT.get()), // 修复材料
        List.of(new ArmorMaterial.Layer(ResourceLocation.fromNamespaceAndPath(MOD_ID, "custom"))), // 纹理层
        0.0F, // 韧性 (Toughness)
        0.0F  // 击退抗性 (Knockback resistance)
    )
);

// 2. 注册盔甲物品并附加 DataComponents (1.21+)
public static final DeferredItem<ArmorItem> CUSTOM_CHESTPLATE = ITEMS.register("custom_chestplate", () -> 
    new ArmorItem(CUSTOM_ARMOR, ArmorItem.Type.CHESTPLATE, new Item.Properties()
        .durability(ArmorItem.Type.CHESTPLATE.getDurability(15)) // 基础耐久乘数
        // 注意：ArmorItem 的构造函数会自动为物品附加 DataComponents.ARMOR。
        // 如果想在非盔甲物品上附加护甲属性，可以手动添加：
        // .component(DataComponents.ARMOR, new ArmorComponent(6, 0.0f, 0.0f))
    )
);
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [物品列表](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#物品列表)
- [获取](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#获取)
  - [合成](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#合成)
  - [锻造](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#锻造)
  - [修复](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#修复)
    - [砂轮](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#砂轮)
    - [铁砧](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#铁砧)
  - [掉落物](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#掉落物)
  - [交易](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#交易)
  - [礼物](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#礼物)
  - [钓鱼](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#钓鱼)
  - [箱子战利品](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#箱子战利品)
- [用途](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#用途)
  - [外观](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#外观)
    - [染色](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#染色)
    - [盔甲纹饰](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#盔甲纹饰)
  - [提供属性](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#提供属性)
  - [提供水下呼吸](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#提供水下呼吸)
  - [躲避猪灵](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#躲避猪灵)
  - [防止冰冻](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#防止冰冻)
  - [魔咒](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#魔咒)
  - [耐久度](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#耐久度)
  - [烧炼材料](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#烧炼材料)
  - [发射器](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#发射器)
  - [减少下落的方块的伤害](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#减少下落的方块的伤害)
- [生物盔甲](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#生物盔甲)
- [音效](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#音效)
- [数据值](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#数据值)
  - [ID](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#ID)
  - [物品数据](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#物品数据)
- [成就](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#成就)
- [进度](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#进度)
- [视频](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#视频)
- [历史](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#历史)
- [你知道吗](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#你知道吗)
- [画廊](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#画廊)
- [参考](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#参考)
- [导航](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#导航)
  - [个人工具](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
