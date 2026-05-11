# Minecraft：属性 (属性)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **属性注册 (Attribute Registration)**：在 NeoForge 1.21+ 中，自定义属性通过 `DeferredRegister<Attribute>` (注册到 `Registries.ATTRIBUTE`) 注册。常用的实现类为 `RangedAttribute`，可定义默认值、最小值和最大值。
- **实体属性绑定 (Entity Attribute Attachment)**：自定义实体必须在 `EntityAttributeCreationEvent` 中绑定初始属性（如最大生命值、移动速度）。若需向原版已有实体（如玩家、僵尸）追加新属性，需在 `EntityAttributeModificationEvent` 中进行。
- **属性修饰符 (Attribute Modifiers) 变更**：1.21+ 的一项重大变更是**彻底移除了使用 UUID 来标识 AttributeModifier**，改为使用 `ResourceLocation` (即 Namespace ID，如 `mymod:weapon_damage`)，这使得修饰符的管理和覆盖更加直观。
- **物品数据组件 (Data Components)**：1.21+ 移除了 NBT 系统。若要为物品添加属性修饰符（如自定义武器的攻击力），必须通过修改物品的 `DataComponents.ATTRIBUTE_MODIFIERS` 数据组件来实现。

---

## 极简代码示例 (Minimal Code Examples)

```java
// 1. 注册自定义属性
public static final DeferredRegister<Attribute> ATTRIBUTES = DeferredRegister.create(Registries.ATTRIBUTE, "mymod");
public static final DeferredHolder<Attribute, Attribute> MANA = ATTRIBUTES.register("mana", 
    () -> new RangedAttribute("attribute.name.mymod.mana", 10.0D, 0.0D, 100.0D).setSyncable(true));

// 2. 为实体绑定或追加属性 (需在模组总线 Mod Event Bus 注册)
@SubscribeEvent
public static void onAttributeCreate(EntityAttributeCreationEvent event) {
    // 为自定义实体设置基础属性
    event.put(MyEntities.CUSTOM_MOB.get(), Mob.createMobAttributes()
        .add(Attributes.MAX_HEALTH, 20.0D)
        .add(MANA.get(), 50.0D).build());
}

@SubscribeEvent
public static void onAttributeModify(EntityAttributeModificationEvent event) {
    // 为原版玩家追加自定义属性
    event.add(EntityType.PLAYER, MANA.get());
}

// 3. 物品的数据组件：添加属性修饰符 (1.21+)
// 注册物品时，使用 Item.Properties 配置数据组件
Item.Properties properties = new Item.Properties()
    .attributes(ItemAttributeModifiers.builder()
        // 1.21+ 使用 ResourceLocation 代替 UUID
        .add(Attributes.ATTACK_DAMAGE, 
             new AttributeModifier(ResourceLocation.fromNamespaceAndPath("mymod", "weapon_damage"), 5.0, AttributeModifier.Operation.ADD_VALUE), 
             EquipmentSlotGroup.MAINHAND)
        .build());
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [属性](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#属性)
- [已知属性项](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#已知属性项)
- [修饰符](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#修饰符)
  - [来源](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#来源)
  - [持久化](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#持久化)
  - [行为](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#行为)
  - [运算模式](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#运算模式)
- [应用](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#应用)
- [历史](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#历史)
- [参考](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#参考)
- [导航](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#导航)
  - [个人工具](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
