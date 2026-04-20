# Minecraft：方块实体 (方块实体)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **数据存储 (NBT Serialization)**：在 1.20.5 及 1.21+ 中，方块实体数据的保存和读取必须传入 `HolderLookup.Provider`。需重写 `saveAdditional`（保存到磁盘）和 `loadAdditional`（从磁盘读取）方法。
- **客户端同步 (Data Synchronization)**：原版使用 `getUpdateTag()` 提供初次加载数据，通过 `getUpdatePacket()` 发送 `ClientboundBlockEntityDataPacket`。如需自定义网络包，也可通过 NeoForge 的自定义 Payload 实现。
- **方块绑定 (Block Binding)**：为了让方块具有方块实体，方块类需实现 `EntityBlock` 接口，并重写 `newBlockEntity` 方法。
- **Tick 逻辑 (Ticking)**：通过在方块类中重写 `getTicker` 方法返回一个 `BlockEntityTicker`，并在其中调用方块实体的静态或实例 tick 方法（分客户端与服务端）。
- **能力系统 (Capabilities)**：NeoForge 1.21+ 弃用了旧版的 `ICapabilityProvider`。现在所有方块实体能力（如物品栏、能量等）均需要通过事件 `RegisterCapabilitiesEvent` 在总线上集中注册。

---

## 极简代码示例 (Minimal Code Examples)

### 1. 方块实体类与数据保存 (Block Entity Class & NBT)

```java
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;

public class MyBlockEntity extends BlockEntity {
    public int customData = 0;

    public MyBlockEntity(BlockPos pos, BlockState state) {
        // 传入由 DeferredRegister 注册的 BlockEntityType
        super(ModBlockEntities.MY_BE.get(), pos, state);
    }

    @Override
    protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.saveAdditional(tag, registries);
        tag.putInt("CustomData", customData);
    }

    @Override
    protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.loadAdditional(tag, registries);
        this.customData = tag.getInt("CustomData");
    }
}
```

### 2. 方块类实现 (EntityBlock & Ticker)

```java
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import org.jetbrains.annotations.Nullable;

public class MyBlock extends Block implements EntityBlock {
    public MyBlock(Properties properties) {
        super(properties);
    }

    @Nullable
    @Override
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new MyBlockEntity(pos, state);
    }

    @Nullable
    @Override
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        if (level.isClientSide()) return null;
        // 仅在服务端执行 Tick 逻辑
        return createTickerHelper(type, ModBlockEntities.MY_BE.get(), 
            (lvl, pos, st, be) -> {
                be.customData++;
                be.setChanged(); // 标记数据已更改以保存
            });
    }

    @SuppressWarnings("unchecked")
    @Nullable
    protected static <E extends BlockEntity, A extends BlockEntity> BlockEntityTicker<A> createTickerHelper(BlockEntityType<A> actual, BlockEntityType<E> expected, BlockEntityTicker<? super E> ticker) {
        return expected == actual ? (BlockEntityTicker<A>) ticker : null;
    }
}
```

### 3. 注册类型与能力 (Registration & Capabilities)

```java
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModBlockEntities {
    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITIES = 
        DeferredRegister.create(BuiltInRegistries.BLOCK_ENTITY_TYPE, "mymod");

    // 注意：1.21 中 build(null) 传入的是 DataFixer 类型，通常填 null
    public static final Supplier<BlockEntityType<MyBlockEntity>> MY_BE = 
        BLOCK_ENTITIES.register("my_be", () -> 
            BlockEntityType.Builder.of(MyBlockEntity::new, ModBlocks.MY_BLOCK.get()).build(null));

    // 在 Mod 事件总线中监听
    public static void registerCapabilities(RegisterCapabilitiesEvent event) {
        // 注册物品栏能力示例
        event.registerBlockEntity(
            Capabilities.ItemHandler.BLOCK,
            MY_BE.get(),
            (be, side) -> be.getItemHandler() // 假设你的 BE 有 getItemHandler() 方法
        );
    }
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [用途](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#用途)
- [方块实体列表](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#方块实体列表)
- [方块实体的渲染距离](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#方块实体的渲染距离)
- [参见](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#参见)
- [导航](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#导航)
  - [个人工具](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
