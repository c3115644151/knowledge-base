# NeoForge 物品交互

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/items/interactions

## 概述

物品交互定义了玩家与物品、实体之间的交互行为，包括右键点击、左键攻击、中键使用等。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `InteractionResult` | 交互结果枚举 |
| `HitResult` | 射线检测结果（BLOCK/ENTITY/MISS） |
| `UseOnContext` | 物品右键使用上下文 |

### InteractionResult 枚举值

| 值 | 说明 |
|----|------|
| `SUCCESS` | 交互成功，消耗操作 |
| `CONSUME` | 交互成功，消耗物品 |
| `FAIL` | 交互失败 |
| `PASS` | 传递给下一个处理器 |
| `TRY_EMPTY_HAND_INTERACTION` | 尝试空手交互 |

---

## 代码示例

### 自定义物品交互

```java
public class CustomItem extends Item {
    public CustomItem() {
        super(Item.Properties.of().stacksTo(64));
    }
    
    @Override
    public InteractionResult useOn(UseOnContext context) {
        // 右键点击方块时触发
        Level level = context.getLevel();
        BlockPos pos = context.getClickedPos();
        Direction face = context.getClickedFace();
        ItemStack stack = context.getItemInHand();
        Player player = context.getPlayer();
        
        // 获取点击位置的方块
        BlockState state = level.getBlockState(pos);
        
        // 在这里添加交互逻辑
        if (!level.isClientSide) {
            // 服务端逻辑
            level.setBlock(pos.relative(face), 
                Blocks.DIAMOND_BLOCK.defaultBlockState());
            stack.shrink(1);
        }
        
        return InteractionResult.SUCCESS;
    }
    
    @Override
    public InteractionResult interactLivingEntity(
            ItemStack stack, 
            Player player, 
            LivingEntity entity,
            InteractionHand hand) {
        // 右键点击生物时触发
        if (!player.level().isClientSide) {
            // 添加自定义逻辑
        }
        return InteractionResult.SUCCESS;
    }
    
    @Override
    public boolean hurtEnemy(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        // 左键攻击生物时触发
        // 返回true表示伤害已处理
        target.addEffect(new MobEffectInstance(
            MobEffects.POISON, 100, 1));
        return true;
    }
    
    @Override
    public boolean mineBlock(ItemStack stack, Level level, 
            BlockState state, BlockPos pos, LivingEntity miner) {
        // 挖掘方块时触发
        if (state.is(Blocks.STONE)) {
            // 挖掘石头时添加逻辑
            return true;
        }
        return false;
    }
}
```

### 物品能力系统 (ItemAbility)

```java
// 定义物品能力
public static final ItemAbility ABILITY_SHIELD_BLOCK = 
    ItemAbility.SHIELD_BLOCK;

// 检查物品是否有某种能力
if (stack.has(ItemAbility.SHIELD_BLOCK)) {
    // 处理盾牌格挡
}

// 自定义物品能力
public static final ItemAbility MY_ABILITY = 
    ItemAbility.register("examplemod:my_ability");

// 获取物品的能力值
Optional<Integer> value = stack.get(ItemAbility.MY_ABILITY);
```

### 使用动画

```java
public class UseAnimationItem extends Item {
    public UseAnimationItem() {
        super(Item.Properties.of()
            .useCooldown(1.0)  // 冷却时间（秒）
        );
    }
    
    @Override
    public ItemDefaultAnimation getUseAnimation(ItemStack stack) {
        return ItemDefaultAnimation.EAT;  // 吃食物动画
        // 或使用: BLOCK, BOW, CROSSBOW, SPEAR, DRINK, NONE
    }
    
    @Override
    public int getUseDuration(ItemStack stack) {
        return 32;  // 使用持续时间(ticks)
    }
    
    @Override
    public UseAction getUseAction(ItemStack stack) {
        return UseAction.EAT;  // 使用动作动画
    }
    
    @Override
    public SoundEvent getEatingSound(ItemStack stack) {
        return SoundEvents.GENERIC_EAT;
    }
    
    @Override
    public ItemStack finishUsingItem(ItemStack stack, Level level, 
            LivingEntity entity) {
        // 使用完成后的逻辑
        if (entity instanceof Player player) {
            player.addEffect(new MobEffectInstance(
                MobEffects.SATURATION, 200));
        }
        return stack.isEdible() ? 
            stack.getCraftingRemainingItem() : stack;
    }
}
```

---

## 注意事项

### 版本差异
- NeoForge 1.21.x 使用 `DataComponent` 系统替代旧版 NBT
- 物品交互结果使用新的 `InteractionResult` 枚举

### 常见错误
1. **交互结果错误**：返回 `PASS` 而非 `SUCCESS` 导致交互无响应
2. **未检查服务端/客户端**：服务端逻辑必须放在 `!level.isClientSide` 分支
3. **物品堆叠问题**：`stack.shrink(1)` 后未检查是否应该消耗

### 最佳实践

```java
@Override
public InteractionResult useOn(UseOnContext context) {
    Level level = context.getLevel();
    if (level.isClientSide) {
        // 客户端：播放音效、粒子等
        return InteractionResult.sidedSuccess(level.isClientSide);
    }
    
    // 服务端：执行实际逻辑
    // ...
    
    return InteractionResult.sidedSuccess(level.isClientSide);
}
```

---

## 关联引用

- 物品注册：[NeoForge-物品](./NeoForge-物品.md)
- 数据组件：[NeoForge-物品-数据组件](./NeoForge-物品-数据组件.md)
- 工具制作：[NeoForge-物品-工具](./NeoForge-物品-工具.md)
