# Minecraft：声音 (声音)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **SoundEvent 注册**：使用 `DeferredRegister<SoundEvent>` 进行注册。在 1.21+ 中，通常通过 `SoundEvent.createVariableRangeEvent(ResourceLocation)` 创建事件实例，使得声音的衰减距离可配置。
- **声音配置 (`sounds.json`)**：自定义音效必须在 `assets/<modid>/sounds.json` 文件中映射。此处定义了音效名称与实际音频文件（`.ogg` 格式，存放在 `assets/<modid>/sounds/` 目录下）的对应关系。
- **服务端与客户端播放**：
  - 在服务端世界播放（广播给周围玩家）：`level.playSound(null, blockPos, MY_SOUND.get(), SoundSource.BLOCKS, 1.0F, 1.0F);`（第一个参数为 null 表示对范围内所有玩家播放）。
  - 在客户端直接播放：利用 `Minecraft.getInstance().getSoundManager().play(...)`。
- **DataGen 数据生成**：推荐使用 NeoForge 提供的 `SoundDefinitionsProvider` 来通过代码自动化生成 `sounds.json`，减少拼写错误。

---

## 极简代码示例 (Minimal Code Examples)

**1. 注册 SoundEvent (核心代码)**
```java
public static final DeferredRegister<SoundEvent> SOUNDS = 
    DeferredRegister.create(BuiltInRegistries.SOUND_EVENT, "mymod");

// 1.21 推荐使用 ResourceLocation.fromNamespaceAndPath
public static final Supplier<SoundEvent> MY_SOUND = SOUNDS.register("my_sound", 
    () -> SoundEvent.createVariableRangeEvent(ResourceLocation.fromNamespaceAndPath("mymod", "my_sound")));
```

**2. 声音配置 (`assets/mymod/sounds.json`)**
```json
{
  "my_sound": {
    "category": "block",
    "subtitle": "mymod.subtitle.my_sound",
    "sounds": [
      "mymod:my_sound_file_1",
      "mymod:my_sound_file_2"
    ]
  }
}
```
*(注：对应的音频文件应放在 `assets/mymod/sounds/my_sound_file_1.ogg` 等路径下。)*

**3. 在世界中播放声音**
```java
// 在服务端或客户端逻辑中调用
level.playSound(
    null,                   // 如果不为 null，则传入的玩家听不到声音（通常传 null 让所有人听到）
    blockPos,               // 声音播放位置
    MY_SOUND.get(),         // 注册的 SoundEvent
    SoundSource.BLOCKS,     // 声音分类（影响玩家设置中的音量滑块）
    1.0F,                   // 音量 (Volume)
    1.0F                    // 音调 (Pitch)
);
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [机制](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#机制)
- [声音分类](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#声音分类)
  - [实体依赖分类](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#实体依赖分类)
- [字幕](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#字幕)
- [数据值](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#数据值)
- [历史](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#历史)
- [画廊](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#画廊)
- [参考](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#参考)
- [导航](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#导航)
  - [个人工具](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
