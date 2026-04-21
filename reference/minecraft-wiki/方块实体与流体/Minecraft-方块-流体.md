# Minecraft：流体 (流体)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **四位一体机制 (The Four Components)**：实现一个完整的自定义流体需要注册四个部分：`FluidType` (NeoForge 属性与渲染)、`Fluid` 源头 (Source)、`Fluid` 流动 (Flowing)、以及流体方块 `LiquidBlock` (在世界中的方块形式)。可选注册对应的桶物品 (`BucketItem`)。
- **FluidType**：这是 NeoForge 添加的流体类型系统，用于统一处理流体的物理属性（如密度、粘度、温度）、声音（如装桶、倒出音效）以及客户端渲染（如材质、雾气颜色）。
- **客户端渲染扩展 (Client Extensions)**：流体的材质纹理、颜色渲染不再在 FluidType 中直接重写，而是通过注册 `IClientFluidTypeExtensions` 并监听 `RegisterClientExtensionsEvent` 来指定。
- **基类使用 (BaseFlowingFluid)**：NeoForge 提供了便捷的 `BaseFlowingFluid` 及其 `Properties` 内部类，极大简化了原版繁琐的流体属性绑定过程。

---

## 极简代码示例 (Minimal Code Examples)

### 1. 流体核心注册 (FluidType & Fluids)

```java
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LiquidBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.neoforge.common.SoundActions;
import net.neoforged.neoforge.fluids.BaseFlowingFluid;
import net.neoforged.neoforge.fluids.FluidType;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;

public class ModFluids {
    public static final String MODID = "mymod";

    // 1. 注册 FluidType
    public static final DeferredRegister<FluidType> FLUID_TYPES = 
        DeferredRegister.create(NeoForgeRegistries.Keys.FLUID_TYPES, MODID);

    public static final Supplier<FluidType> MY_FLUID_TYPE = FLUID_TYPES.register("my_fluid", () -> 
        new FluidType(FluidType.Properties.create()
            .density(1000)
            .viscosity(1000)
            .sound(SoundActions.BUCKET_FILL, SoundEvents.BUCKET_FILL)
            .sound(SoundActions.BUCKET_EMPTY, SoundEvents.BUCKET_EMPTY)));

    // 2. 注册 Fluid
    public static final DeferredRegister<Fluid> FLUIDS = 
        DeferredRegister.create(BuiltInRegistries.FLUID, MODID);

    public static final Supplier<FlowingFluid> MY_FLUID_SOURCE = FLUIDS.register("my_fluid", 
        () -> new BaseFlowingFluid.Source(MY_FLUID_PROPERTIES));
    
    public static final Supplier<FlowingFluid> MY_FLUID_FLOWING = FLUIDS.register("my_fluid_flowing", 
        () -> new BaseFlowingFluid.Flowing(MY_FLUID_PROPERTIES));

    // 3. 注册 LiquidBlock (需与 Blocks 的 DeferredRegister 配合)
    public static final Supplier<LiquidBlock> MY_FLUID_BLOCK = ModBlocks.BLOCKS.register("my_fluid_block", 
        () -> new LiquidBlock(MY_FLUID_SOURCE.get(), BlockBehaviour.Properties.ofFullCopy(Blocks.WATER)));

    // 4. 定义 Properties 绑定以上所有元素 (注意要使用懒加载/延迟获取)
    public static final BaseFlowingFluid.Properties MY_FLUID_PROPERTIES = new BaseFlowingFluid.Properties(
        MY_FLUID_TYPE, MY_FLUID_SOURCE, MY_FLUID_FLOWING
    ).block(MY_FLUID_BLOCK); // 如果有桶，还可加上 .bucket(ModItems.MY_FLUID_BUCKET)
}
```

### 2. 客户端材质渲染扩展 (Client Extensions)

```java
import net.minecraft.resources.ResourceLocation;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.extensions.common.IClientFluidTypeExtensions;
import net.neoforged.neoforge.client.extensions.common.RegisterClientExtensionsEvent;

@EventBusSubscriber(modid = ModFluids.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public class ModClientEvents {

    @SubscribeEvent
    public static void onRegisterClientExtensions(RegisterClientExtensionsEvent event) {
        event.registerFluidType(new IClientFluidTypeExtensions() {
            private static final ResourceLocation STILL = ResourceLocation.fromNamespaceAndPath("mymod", "block/my_fluid_still");
            private static final ResourceLocation FLOWING = ResourceLocation.fromNamespaceAndPath("mymod", "block/my_fluid_flow");

            @Override
            public ResourceLocation getStillTexture() {
                return STILL;
            }

            @Override
            public ResourceLocation getFlowingTexture() {
                return FLOWING;
            }
        }, ModFluids.MY_FLUID_TYPE.get());
    }
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [属性](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#属性)
  - [概览](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#概览)
  - [机制](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#机制)
    - [深度](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#深度)
    - [扩散](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#扩散)
    - [流动方向](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#流动方向)
  - [液滴](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#液滴)
  - [方块更新](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#方块更新)
  - [液体互动](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#液体互动)
- [历史](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#历史)
- [画廊](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#画廊)
- [参考](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#参考)
- [导航](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#导航)
  - [个人工具](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
