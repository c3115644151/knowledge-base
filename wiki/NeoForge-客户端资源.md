# NeoForge 客户端资源

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/client/

## 概述

客户端资源包括纹理、模型、音效、粒子等，用于定义游戏的外观和声音表现。

## 子主题

### 纹理系统
- [国际化与本地化](./NeoForge-客户端-国际化.md)
- [纹理](./NeoForge-客户端-纹理.md)
- [模型](./NeoForge-客户端-模型.md)
- [音效](./NeoForge-客户端-音效.md)
- [粒子](./NeoForge-客户端-粒子.md)

## 资源文件位置

```
assets/<namespace>/
├── lang/                    # 语言文件
│   └── en_us.json
├── textures/                # 纹理
│   ├── block/
│   ├── entity/
│   ├── item/
│   └── particle/
├── models/                  # 模型
│   ├── block/
│   ├── item/
│   └── entity/
├── sounds.json             # 音效定义
└── neoforge/
    └── animations/         # 动画定义
```

---

## 客户端代理模式

```java
// 1. 创建客户端代理
@Mod(MOD_ID)
public class ExampleMod {
    public ExampleMod() {
        IEventBus modBus = FMLJavaModLoadingContext.get()
            .getModEventBus();
        
        // 在 mod 总线上注册
        modBus.addListener(this::clientSetup);
    }
    
    private void clientSetup(final FMLClientSetupEvent event) {
        // 客户端初始化
    }
}

// 2. 使用 Dist 注解
@Mod.EventBusSubscriber(modid = MOD_ID, 
    bus = Mod.EventBusSubscriber.Bus.MOD, 
    value = Dist.CLIENT)
public class ClientOnly {
    @SubscribeEvent
    public static void init(RegisterClientHandlersEvent event) {
        // 注册客户端处理器
    }
}
```

---

## 关联引用

- 服务端资源：[NeoForge-服务端资源](./NeoForge-服务端资源.md)
- 渲染系统：[NeoForge-渲染-特性](./NeoForge-渲染-特性.md)
