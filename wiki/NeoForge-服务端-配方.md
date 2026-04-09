# NeoForge-服务端-配方

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/server/recipes/

## 概述

配方是将一组对象转换为其他对象的方式。虽然 Minecraft 将此系统用于物品转换，但系统设计允许任何类型的对象（方块、实体等）进行转换。

配方文件位于 `data/<namespace>/recipe/<path>.json`。

## 术语

- **Recipe JSON**：配方 JSON 文件
- **Recipe**：配方类，包含匹配逻辑
- **RecipeInput**：配方输入
- **Ingredient**：配方材料
- **RecipeType**：配方类型
- **RecipeSerializer**：配方序列化器

## JSON 结构

```json
{
    "type": "minecraft:crafting_shaped",
    "group": "wooden_fences",
    "pattern": [
        "###",
        "###"
    ],
    "key": {
        "#": {"item": "minecraft:stick"}
    },
    "result": {
        "item": "minecraft:oak_fence",
        "count": 3
    }
}
```

## 配方类型

| 类型 | 说明 |
|------|------|
| `minecraft:crafting_shaped` | 成形合成 |
| `minecraft:crafting_shapeless` | 随机合成 |
| `minecraft:smelting` | 熔炉烧制 |
| `minecraft:blasting` | 高炉烧制 |
| `minecraft:smoking` | 烟熏炉 |
| `minecraft:campfire_cooking` | 营火烹饪 |
| `minecraft:stonecutting` | 切石 |
| `minecraft:smithing_transform` | 锻造转换 |
| `minecraft:smithing_trim` | 锻造装饰 |

## 成形合成 (Shaped)

```json
{
    "type": "minecraft:crafting_shaped",
    "pattern": [
        "###",
        " # ",
        " # "
    ],
    "key": {
        "#": {"item": "minecraft:stick"}
    },
    "result": {
        "item": "minecraft:ladder",
        "count": 3
    }
}
```

## 随机合成 (Shapeless)

```json
{
    "type": "minecraft:crafting_shapeless",
    "ingredients": [
        {"item": "minecraft:oak_planks"},
        {"item": "minecraft:oak_planks"}
    ],
    "result": {
        "item": "minecraft:stick",
        "count": 4
    }
}
```

## 熔炉配方 (Smelting)

```json
{
    "type": "minecraft:smelting",
    "ingredient": {"item": "minecraft:iron_ore"},
    "result": "minecraft:iron_ingot",
    "experience": 0.7,
    "cookingtime": 200
}
```

## 使用配方

```java
// 获取配方管理器
RecipeManager recipes = server.getRecipeManager();

// 获取所有配方
Map<ResourceKey<Recipe<?>>, Recipe<?>> allRecipes = recipes.getRecipes();

// 获取特定配方
recipes.getRecipeById(ResourceKey.create(Registries.RECIPE, Identifier.of("minecraft", "diamond_block")));

// 检查配方是否匹配
CraftingInput input = ...;
recipes.getRecipeFor(input, server.getLevel());
```

## 自定义配方类型

### 创建配方

```java
public class MyRecipe implements Recipe<CraftingInput> {
    @Override
    public boolean matches(CraftingInput input, Level level) {
        // 匹配逻辑
    }

    @Override
    public ItemStack assemble(CraftingInput input, HolderLookup.Provider registries) {
        // 合成逻辑
    }

    @Override
    public boolean canCraftInDimensions(int width, int height) {
        return width * height >= 9;
    }

    @Override
    public ItemStack getResultItem(HolderLookup.Provider registries) {
        return ItemStack.EMPTY;
    }

    @Override
    public RecipeSerializer<?> getSerializer() {
        return MyRecipeSerializer.INSTANCE;
    }

    @Override
    public RecipeType<?> getType() {
        return TYPE;
    }
}
```

### 创建序列化器

```java
public class MyRecipeSerializer implements RecipeSerializer<MyRecipe> {
    public static final MyRecipeSerializer INSTANCE = new MyRecipeSerializer();
    
    @Override
    public void encode(FriendlyByteBuf buffer, MyRecipe recipe) {
        // 编码
    }

    @Override
    public MyRecipe decode(FriendlyByteBuf buffer) {
        // 解码
    }
}
```

### 注册

```java
public static final DeferredRegister<RecipeSerializer<?>> SERIALIZERS = 
    DeferredRegister.create(Registries.RECIPE_SERIALIZER, MODID);

public static final RegistryObject<MyRecipeSerializer> MY_RECIPE = 
    SERIALIZERS.register("my_recipe", () -> MyRecipeSerializer.INSTANCE);
```

## 数据生成

```java
public class MyRecipeProvider extends RecipeProvider {
    public MyRecipeProvider(PackOutput output, CompletableFuture<HolderLookup.Provider> lookupProvider) {
        super(output, lookupProvider);
    }

    @Override
    protected void buildRecipes(Consumer<FinishedRecipe> consumer) {
        ShapedRecipeBuilder.shaped(consumer, ItemStack(Items.DIAMOND))
            .pattern("###")
            .pattern("#D#")
            .pattern("###")
            .define('#', Items.IRON_INGOT)
            .define('D', Items.DIAMOND)
            .unlockedBy("has_item", has(Items.DIAMOND))
            .save(consumer);
    }
}
```

## 注意事项

1. **配方在服务端运行**：配方逻辑应在服务端执行
2. **材料匹配**：使用 Ingredient 系统进行灵活匹配
3. **经验值**：烧制类配方可设置经验值
4. **配方解锁**：配方可以关联进度解锁

## 关联引用

- [[NeoForge-服务端资源]] - 服务端资源总览
- [[NeoForge-服务端-材料]] - 配方材料系统
- [[NeoForge-服务端-进度]] - 配方解锁进度
