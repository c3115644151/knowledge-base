# NeoForge-物品栏-容器

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/inventories/container

## 概述

容器（Container）用于在 BlockEntity 或其他对象上存储物品。

## 基本 Container 实现

```java
public class MyContainer implements Container {
    private final NonNullList<ItemStack> items = NonNullList.withSize(27, ItemStack.EMPTY);

    @Override
    public int getContainerSize() {
        return 27;
    }

    @Override
    public boolean isEmpty() {
        return this.items.stream().allMatch(ItemStack::isEmpty);
    }

    @Override
    public ItemStack getItem(int slot) {
        return this.items.get(slot);
    }

    @Override
    public void setItem(int slot, ItemStack stack) {
        stack.limitSize(this.getMaxStackSize(stack));
        this.items.set(slot, stack);
        this.setChanged();
    }

    @Override
    public ItemStack removeItem(int slot, int amount) {
        ItemStack stack = ContainerHelper.removeItem(this.items, slot, amount);
        this.setChanged();
        return stack;
    }

    @Override
    public ItemStack removeItemNoUpdate(int slot) {
        ItemStack stack = ContainerHelper.takeItem(this.items, slot);
        this.setChanged();
        return stack;
    }

    @Override
    public void setChanged() {
        // 通知 BlockEntity 数据已更改
    }

    @Override
    public boolean stillValid(Player player) {
        return true;
    }

    @Override
    public void clearContent() {
        this.items.clear();
        this.setChanged();
    }
}
```

## SimpleContainer

`SimpleContainer` 是带有额外功能的基本实现：

```java
SimpleContainer container = new SimpleContainer(27);
container.addListener(listener);  // 添加监听器
```

## BaseContainerBlockEntity

方块实体的便捷基类：

```java
public class MyBlockEntity extends BaseContainerBlockEntity {
    public static final int SIZE = 9;
    private NonNullList<ItemStack> items = NonNullList.withSize(SIZE, ItemStack.EMPTY);

    public MyBlockEntity(BlockPos pos, BlockState blockState) {
        super(MY_BLOCK_ENTITY.get(), pos, blockState);
    }

    @Override
    public int getContainerSize() {
        return SIZE;
    }

    @Override
    protected NonNullList<ItemStack> getItems() {
        return items;
    }

    @Override
    protected void setItems(NonNullList<ItemStack> items) {
        this.items = items;
    }

    @Override
    protected Component getDefaultName() {
        return Component.translatable("container.examplemod.myblockentity");
    }

    @Override
    protected AbstractContainerMenu createMenu(int containerId, Inventory inventory) {
        return null; // 返回菜单或 null
    }
}
```

## WorldlyContainer

允许按方向访问槽位：

```java
public class MyBlockEntity extends BaseContainerBlockEntity implements WorldlyContainer {
    private static final int[] OUTPUTS = new int[]{0};
    private static final int[] INPUTS = new int[]{1, 2, 3, 4, 5, 6, 7, 8};

    @Override
    public int[] getSlotsForFace(Direction side) {
        return side == Direction.UP ? OUTPUTS : INPUTS;
    }

    @Override
    public boolean canPlaceItemThroughFace(int index, ItemStack stack, @Nullable Direction direction) {
        return direction != Direction.UP && index > 0 && index < 9;
    }

    @Override
    public boolean canTakeItemThroughFace(int index, ItemStack stack, Direction direction) {
        return direction == Direction.UP && index == 0;
    }
}
```

## Container 在 ItemStack 上

使用 `minecraft:container` 数据组件：

```java
public class MyBackpackContainer extends SimpleContainer {
    private final ItemStack stack;

    public MyBackpackContainer(ItemStack stack) {
        super(27);
        this.stack = stack;
        ItemContainerContents contents = stack.getOrDefault(DataComponents.CONTAINER, ItemContainerContents.EMPTY);
        contents.copyInto(this.getItems());
    }

    @Override
    public void setChanged() {
        super.setChanged();
        this.stack.set(DataComponents.CONTAINER, ItemContainerContents.fromItems(this.getItems()));
    }
}
```

## Container 在 Entity 上

### Mob 装备

```java
// 获取装备槽位
ItemStack helmet = mob.getItemBySlot(EquipmentSlot.HEAD);
mob.setItemSlot(EquipmentSlot.FEET, new ItemStack(Items.BEDROCK));
mob.setDropChance(EquipmentSlot.FEET, 1f);
```

### 玩家物品栏

```java
Inventory playerInv = player.getInventory();
// 主要物品栏槽位 0-35
// 装备槽位通过 EQUIPMENT_SLOT_MAPPING
```

## API 速查表

| 方法 | 说明 |
|------|------|
| `getContainerSize()` | 获取槽位数量 |
| `isEmpty()` | 是否为空 |
| `getItem(slot)` | 获取槽位物品 |
| `setItem(slot, stack)` | 设置槽位物品 |
| `removeItem(slot, amount)` | 移除物品 |
| `removeItemNoUpdate(slot)` | 移除所有物品 |
| `stillValid(player)` | 玩家是否有效 |
| `clearContent()` | 清空容器 |
| `setChanged()` | 标记为已更改 |

## 注意事项

1. **NeoForge 推荐**：优先使用 `ItemStacksResourceHandler`
2. **BlockEntity 实现**：实现 Container 会自动处理掉落
3. **槽位边界**：访问超出范围的槽位可能抛出异常
4. **不可变性**：提交到菜单的 ItemStack 必须 `#copy()`

## 关联引用

- [[NeoForge-方块实体]] - BlockEntity 基础
- [[NeoForge-物品栏-菜单]] - 容器菜单
- [[NeoForge-物品]] - 物品系统
