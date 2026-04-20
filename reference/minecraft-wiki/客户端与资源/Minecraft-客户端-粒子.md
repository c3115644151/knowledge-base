# Minecraft：粒子 (粒子)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **粒子类型注册**：使用 `DeferredRegister<ParticleType<?>>` 注册。常见的简单粒子使用 `SimpleParticleType`。
- **粒子提供者注册**：NeoForge 1.21+ 中，必须在**客户端 Mod 事件总线**（`@EventBusSubscriber(bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)`）中监听 `RegisterParticleProvidersEvent`，使用 `event.registerSpriteSet()` 或 `event.registerSpecial()` 注册自定义粒子的渲染逻辑（Provider）。
- **粒子纹理定义**：粒子的纹理序列需在 `assets/<modid>/particles/<particle_name>.json` 中配置，无需代码硬编码。纹理图片放置在 `assets/<modid>/textures/particle/` 目录下。
- **生成粒子**：在客户端使用 `level.addParticle()` 生成；在服务端使用 `serverLevel.sendParticles()` 将粒子同步给客户端。

---

## 极简代码示例 (Minimal Code Examples)

**1. 注册粒子类型 (核心代码)**
```java
public static final DeferredRegister<ParticleType<?>> PARTICLE_TYPES = 
    DeferredRegister.create(BuiltInRegistries.PARTICLE_TYPE, "mymod");

// 参数 true 表示粒子在最小粒子设置下始终显示 (alwaysShow)
public static final Supplier<SimpleParticleType> MY_PARTICLE = 
    PARTICLE_TYPES.register("my_particle", () -> new SimpleParticleType(true));
```

**2. 绑定 Provider (客户端代码)**
```java
@EventBusSubscriber(modid = "mymod", bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public class ClientModEvents {
    @SubscribeEvent
    public static void onRegisterParticleProviders(RegisterParticleProvidersEvent event) {
        // registerSpriteSet 允许粒子读取 assets/mymod/particles/my_particle.json 中的纹理
        event.registerSpriteSet(MY_PARTICLE.get(), MyParticleProvider::new);
    }
}
```

**3. 粒子 JSON (`assets/mymod/particles/my_particle.json`)**
```json
{
  "textures": [
    "mymod:my_particle_0",
    "mymod:my_particle_1"
  ]
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [定义](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#定义)
- [行为](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#行为)
- [类型](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#类型)
  - [带选项粒子](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#带选项粒子)
  - [简单粒子](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#简单粒子)
- [历史](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#历史)
- [你知道吗](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#你知道吗)
- [画廊](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#画廊)
- [参考](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#参考)
- [导航](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#导航)
  - [个人工具](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
