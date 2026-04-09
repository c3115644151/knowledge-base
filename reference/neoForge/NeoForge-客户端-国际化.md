# NeoForge 客户端国际化

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/client/i18n

## 概述

国际化（I18n）和本地化（L10n）系统用于处理游戏中的文本显示，包括组件（Component）、样式（Style）和翻译键。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `Component` | 文本组件 |
| `Style` | 样式定义 |
| `MutableComponent` | 可变组件 |
| `TranslatableContents` | 可翻译内容 |

---

## 代码示例

### 基本文本组件

```java
// 1. 纯文本
Component text = Component.literal("Hello World");

// 2. 可翻译文本
Component translated = Component.translatable("item.diamond.name");

// 3. 带样式的文本
Component styled = Component.literal("Bold Text")
    .withStyle(style -> style.withBold(true));

// 4. 颜色和格式
Component colored = Component.literal("Red Text")
    .withColor(0xFF0000);

Component underlined = Component.literal("Underlined")
    .withStyle(s -> s.withUnderlined(true));
```

### 翻译组件

```java
// 1. 带参数的翻译
Component withArgs = Component.translatable(
    "entity.minecraft.pig",
    Component.literal("MyPig"),  // %s 参数
    42                           // %d 参数
);

// 2. 带样式的翻译
Component styledTranslatable = Component.translatable("key.example")
    .withStyle(style -> style
        .withColor(ChatFormatting.GOLD)
        .withBold(true)
        .withHoverEvent(new HoverEvent(
            HoverEvent.Action.SHOW_TEXT,
            Component.literal("Hover!")))
        .withClickEvent(new ClickEvent(
            ClickEvent.Action.RUN_COMMAND,
            "/say Hello")));

// 3. 动态翻译内容
TranslatableContents contents = new TranslatableContents(
    "container.inventory",
    null,  // 无参数
    Style.EMPTY,
    List.of(
        Component.literal("Main"),
        Component.literal("Armor")
    )
);
Component dynamic = new TextComponent(contents);
```

### 样式（Style）

```java
// 1. 完整样式
Style style = Style.EMPTY
    .withColor(0x00FF00)
    .withBold(true)
    .withItalic(false)
    .withUnderlined(true)
    .withStrikethrough(false)
    .withObfuscated(true)
    .withFont(ResourceLocation.fromNamespaceAndPath(MOD_ID, "custom"))
    .withInsertion("text_to_insert")
    .withHoverEvent(new HoverEvent(
        HoverEvent.Action.SHOW_TEXT,
        Component.literal("Hover tooltip")))
    .withClickEvent(new ClickEvent(
        ClickEvent.Action.SUGGEST_COMMAND,
        "/tellraw @s Hello"));

// 2. 字体资源
// assets/<namespace>/font/<font_name>.json

// 3. Hover 事件
HoverEvent hoverEvent = new HoverEvent(
    HoverEvent.Action.SHOW_TEXT,
    Component.literal("Tooltip content"));

// 4. Click 事件
ClickEvent clickEvent = new ClickEvent(
    ClickEvent.Action.RUN_COMMAND,
    "/say Hello");

// 5. .shiftClick 事件
StringShiftClickEvent shiftClickEvent = 
    StringShiftClickEvent.forText(
        Component.literal("Shift-clicked text"));
```

### 组件操作

```java
// 1. 遍历组件
Component root = Component.translatable("menu.multiplayer");
root.visit((style, text) -> {
    // 处理每个文本段
    return Optional.empty();
}, Style.EMPTY);

// 2. 复制组件
Component copy = original.copy();

// 3. 合并组件
MutableComponent merged = Component.empty();
merged.append(Component.literal("A"));
merged.append(Component.literal("B"));
merged.append(Component.literal("C"));

// 4. 替换文本
Component replaced = Component.translatable("gui.obsidian")
    .replace("-", Component.literal("_"));
```

### 事件监听

```java
// 1. 格式化工具提示
@SubscribeEvent
public static void onItemStackTooltip(
        ItemStackTooltipEvent event) {
    if (event.getItemStack().is(Items.DIAMOND)) {
        event.getTooltips().add(
            Component.translatable(
                "tooltip.examplemod.diamond_extra",
                event.getItemStack().getCount()
            ).withColor(ChatFormatting.AQUA)
        );
    }
}

// 2. 格式化工具提示图标
@SubscribeEvent
public static void onTooltipImage(
        TooltipRenderEvent.DrawStandard event) {
    // 绘制自定义图标
}
```

---

## 语言文件

### JSON 格式

```json
// assets/examplemod/lang/en_us.json
{
    "item.examplemod.example_item": "Example Item",
    "item.examplemod.example_item.desc": "A fancy example item",
    
    "entity.examplemod.example_entity": "Example Entity",
    
    "block.examplemod.example_block": "Example Block",
    
    "itemGroup.examplemod.tab": "Example Mod Items",
    
    "tooltip.examplemod.holding": "Holding: %s",
    "tooltip.examplemod.count": "Count: %d",
    "tooltip.examplemod.multi": "%s x %d",
    
    "death.attack.examplemod.custom": "%1$s was vaporized"
}
```

### 数据生成

```java
// 1. 创建语言提供者
@Mod.EventBusSubscriber(modid = MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public static class LangGen {
    @SubscribeEvent
    public static void gatherData(GatherDataEvent event) {
        event.createProvider((output, lookupProvider) ->
            new LanguageProvider(
                output,
                "en_us",       // 语言代码
                "en"           // 区域代码
            )
        );
    }
}

// 2. 扩展语言生成器
public class ModLanguageProvider extends LanguageProvider {
    public ModLanguageProvider(PackOutput output,
            String languageId, String regionId) {
        super(output, languageId, regionId);
    }
    
    @Override
    protected void addTranslations(TranslationData data) {
        add("item.examplemod.example_item", "Example Item");
        add("block.examplemod.example_block", "Example Block");
        add("entity.examplemod.example_entity", "Example Entity");
    }
}

// 3. 注册提供者
@SubscribeEvent
public static void gatherData(GatherDataEvent event) {
    event.createProvider((output, lookupProvider) ->
        new ModLanguageProvider(output, "en_us", "en")
    );
}
```

---

## 注意事项

### 翻译键命名
- 使用小写和下划线
- 遵循 `category.name.subname` 结构
- 使用 Minecraft 命名约定

### 常见错误
1. **翻译不显示**：检查 JSON 文件路径和格式
2. **参数错误**：确认参数类型和数量
3. **样式不生效**：检查 `withStyle` 调用顺序

### 最佳实践

```java
// 推荐：使用常量定义翻译键
public static class TranslationKeys {
    public static final String ITEM = "item.examplemod.item";
    public static final String TOOLTIP = "tooltip.examplemod.holding";
}

// 使用
Component itemName = Component.translatable(TranslationKeys.ITEM);
```

---

## 关联引用

- 物品：[NeoForge-物品](./NeoForge-物品.md)
- 组件系统：[相关文档]
