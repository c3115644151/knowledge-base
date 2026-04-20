# Minecraft 数据驱动：标签 (Tags)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/Java版标签](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

在 NeoForge 1.21+ 开发中，**标签 (Tags)** 是将游戏资源（方块、物品、实体、流体、魔咒等）进行分组的唯一标准方式。强烈建议**避免在代码中硬编码 `block == Blocks.STONE`**，而是使用标签（如 `#minecraft:stone_ore_replaceables`），以确保模组间的兼容性。

### NeoForge 对照文档

- [NeoForge-服务端-标签](../../neoForge/NeoForge-服务端-标签.md)

### 1. 注册表与标识符
- **标识符表示**：在 JSON 和命令中，标签以 `#` 开头（如 `#minecraft:logs`）。
- **代码中表示**：使用 `TagKey<T>` 表示。
  - 创建方法：`TagKey.create(Registries.BLOCK, ResourceLocation.fromNamespaceAndPath("mymod", "my_blocks"))`
- **文件路径**：`data/<namespace>/tags/<registry_path>/<name>.json`
  - 常见路径：`tags/block/`, `tags/item/`, `tags/entity_type/`, `tags/enchantment/` 等。

### 2. 数据驱动的标签定义 (JSON 结构)
标签本质上是一个资源 ID 列表，并支持包含其他标签：
- `replace`: 布尔值（默认为 `false`）。
  - 若为 `false`，则将当前列表追加到现有同名标签中（模组通常使用此模式来扩展原版标签）。
  - 若为 `true`，则覆盖低优先级数据包中定义的同名标签（极不推荐模组使用）。
- `values`: 包含 ID 或其他标签的数组。
  - 元素可以是一个字符串 `"minecraft:stone"` 或 `"#minecraft:base_stone_overworld"`。
  - 也可以是一个带有 `id` 和 `required` 属性的对象：`{"id": "othermod:custom_stone", "required": false}`。如果依赖的模组未安装，将静默忽略而不会报错。

### 3. 数据生成器 (DataGen)
NeoForge 提供了全面的 Datagen 支持生成标签：
- **核心类**：继承 `TagsProvider<T>` 的子类。
  - 方块标签：`BlockTagsProvider`
  - 物品标签：`ItemTagsProvider`（注意：物品标签通常依赖方块标签以自动同步，可以通过 `copy(BlockTag, ItemTag)` 快速复制方块到物品标签）。
  - 实体类型标签：`EntityTypeTagsProvider`
- **用法示例**：
  ```java
  @Override
  protected void addTags(HolderLookup.Provider provider) {
      // 创建自定义标签并添加元素
      this.tag(MyTags.Blocks.MY_CUSTOM_BLOCKS)
          .add(MyBlocks.MAGIC_BLOCK.get())
          .addOptional(ResourceLocation.parse("othermod:magic_block"));
          
      // 将模组方块添加到原版标签（挖掘等级）
      this.tag(BlockTags.MINEABLE_WITH_PICKAXE)
          .addTag(MyTags.Blocks.MY_CUSTOM_BLOCKS);
          
      this.tag(BlockTags.NEEDS_IRON_TOOL)
          .add(MyBlocks.MAGIC_BLOCK.get());
  }
  ```

### 4. 代码层面的交互
在代码中判断资源是否属于某个标签：
- **方块状态**：`blockState.is(BlockTags.LOGS)`
- **物品堆**：`itemStack.is(ItemTags.LOGS)`
- **实体类型**：`entityType.is(EntityTypeTags.SKELETONS)`
- **通用 Holder (1.21+)**：对于魔咒、生物群系等注册表，通常通过 `Holder<T>` 进行判断：`enchantmentHolder.is(EnchantmentTags.TREASURE)`。

### 5. 常见开发避坑指南
- **物品标签与方块标签混淆**：`ItemTags` 和 `BlockTags` 是完全独立的！`BlockTags.LOGS` 不能用于判断 `ItemStack`，即使它们同名。在 Datagen 中记得使用 `copy()` 方法同步方块标签到物品标签。
- **缺失 `required: false` 导致崩溃**：在 JSON 中直接写 `othermod:item` 时，如果 `othermod` 未安装，标签解析将失败，整个标签失效。如果是跨模组联动，务必使用对象格式并设置 `required: false`（在 Datagen 中对应 `addOptional()`）。

---

## 极简代码示例 (Minimal Code Examples)

### 1. 标签 Datagen (Java)
```java
public class MyBlockTagsProvider extends BlockTagsProvider {
    public MyBlockTagsProvider(PackOutput output, CompletableFuture<HolderLookup.Provider> lookupProvider, ExistingFileHelper existingFileHelper) {
        super(output, lookupProvider, MyMod.MODID, existingFileHelper);
    }

    @Override
    protected void addTags(HolderLookup.Provider provider) {
        // 创建自定义标签并添加元素
        TagKey<Block> MY_BLOCKS = BlockTags.create(ResourceLocation.fromNamespaceAndPath(MyMod.MODID, "my_blocks"));
        
        this.tag(MY_BLOCKS)
            .add(MyBlocks.CUSTOM_BLOCK.get())
            .addOptional(ResourceLocation.parse("othermod:other_block"));

        // 将自定义标签加入原版标签（例如挖掘等级）
        this.tag(BlockTags.MINEABLE_WITH_PICKAXE)
            .addTag(MY_BLOCKS);
    }
}
```

### 2. 标签定义 (JSON)
`data/mymod/tags/block/my_blocks.json`
```json
{
  "replace": false,
  "values": [
    "mymod:custom_block",
    {
      "id": "othermod:other_block",
      "required": false
    },
    "#minecraft:stone_ore_replaceables"
  ]
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版标签的目录结构、加载机制和详尽列表，请直接通过以下锚点跳转至 Wiki 原文查阅。

### 1. 基础结构与机制
- [目录结构](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84) *(定义标签存放的数据包路径)*
- [文件格式与命名空间](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E6%96%87%E4%BB%B6%E6%A0%BC%E5%BC%8F) *(JSON 的结构与 `#` 符号)*
- [加载行为 (Loading Behavior)](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E5%8A%A0%E8%BD%BD%E8%A1%8C%E4%B8%BA) *(多数据包合并、覆盖与错误处理)*

### 2. 原版内置标签字典 (完整列表)
> **以下为开发中高频使用的原版标签类别大全：**

- [**方块标签 (Block Tags)**](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE/%E6%96%B9%E5%9D%97) *(包含可攀爬、挖掘工具要求、防火等分类)*
- [**物品标签 (Item Tags)**](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE/%E7%89%A9%E5%93%81) *(包含燃料、染料、盔甲、食物分类)*
- [**实体类型标签 (Entity Type Tags)**](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE/%E5%AE%9E%E4%BD%93%E7%B1%BB%E5%9E%8B) *(节肢生物、亡灵、抗火实体)*
- [**流体标签 (Fluid Tags)**](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE/%E6%B5%81%E4%BD%93) *(水、熔岩等)*
- [**魔咒标签 (Enchantment Tags)**](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE/%E9%AD%94%E5%92%92) *(1.21+ 新增，控制互斥、宝藏魔咒、可附魔性等)*
- [**生物群系标签 (Biome Tags)**](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB) *(群系生成和生物生成的过滤条件)*

### 3. 其他进阶标签
- [伤害类型 (Damage Type)](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE/%E4%BC%A4%E5%AE%B3%E7%B1%BB%E5%9E%8B) *(1.20+，用于判定伤害抗性或触发效果)*
- [函数标签 (Function Tags)](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE/%E5%87%BD%E6%95%B0) *(例如 `#minecraft:tick` 和 `#minecraft:load` 用于数据包)*
- [游戏事件 (Game Event)](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE/%E6%B8%B8%E6%88%8F%E4%BA%8B%E4%BB%B6) *(用于幽匿感测体监听机制)*

### Wiki 全目录（H2/H3/H4）

- [定义](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E5%AE%9A%E4%B9%89)
  - [目录结构](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84)
  - [命名空间ID](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E5%91%BD%E5%90%8D%E7%A9%BA%E9%97%B4ID)
  - [文件格式](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E6%96%87%E4%BB%B6%E6%A0%BC%E5%BC%8F)
  - [加载行为](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E5%8A%A0%E8%BD%BD%E8%A1%8C%E4%B8%BA)
- [使用](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E4%BD%BF%E7%94%A8)
  - [原版标签](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E5%8E%9F%E7%89%88%E6%A0%87%E7%AD%BE)
  - [示例](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E7%A4%BA%E4%BE%8B)
- [历史](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E5%8E%86%E5%8F%B2)
- [你知道吗](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E4%BD%A0%E7%9F%A5%E9%81%93%E5%90%97)
- [参见](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E5%8F%82%E8%A7%81)
- [导航](https://zh.minecraft.wiki/w/Java%E7%89%88%E6%A0%87%E7%AD%BE#%E5%AF%BC%E8%88%AA)

---

## 相关资源与材质 (Assets)

标签本身不对应贴图资源，但它会深度影响“哪些资源被视为一类”，从而影响：
- **方块/物品行为**：工具挖掘判定、燃料判定、可附魔判定、可作为配方材料等
- **数据文件路径**：`data/<namespace>/tags/<registry>/<tag>.json`
