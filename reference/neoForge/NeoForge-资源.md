# NeoForge 资源系统

## 资源类型

| 类型 | 路径 | 说明 |
|------|------|------|
| **Assets** (资源) | `assets/` | 仅客户端（纹理、模型、翻译、声音） |
| **Data** (数据) | `data/` | 服务端（战利品表、配方、进度） |

NeoForge 自动为每个 mod 生成内置资源/数据包。

---

## 资源包 (Assets)

### 目录结构

```
assets/
├── minecraft/
│   ├── textures/
│   ├── models/
│   └── lang/
└── mymodid/
    ├── textures/
    │   ├── block/example_block.png
    │   └── item/example_item.png
    ├── models/
    │   ├── block/example_block.json
    │   └── item/example_item.json
    ├── lang/
    │   └── en_us.json
    └── sounds/
        └── definitions.json
```

### 常用 Assets 路径

| 文件夹 | 内容 |
|--------|------|
| `atlases` | 纹理图集源 |
| `blockstates` | 方块状态 JSON |
| `models` | 模型 JSON |
| `textures` | PNG 纹理 |
| `lang` | 翻译文件 |
| `sounds` | 声音定义 |
| `particles` | 粒子定义 |

---

## 数据包 (Data Pack)

### 目录结构

```
data/
├── minecraft/
│   ├── loot_tables/
│   ├── recipes/
│   ├── tags/
│   └── advancements/
└── mymodid/
    ├── my_custom_registry/
    └── ...
```

### 常用 Data 路径

| 文件夹 | 内容 |
|--------|------|
| `loot_table` | 战利品表 |
| `recipe` | 合成配方 |
| `advancement` | 进度 |
| `tags` | 标签 |
| `damage_type` | 伤害类型 |
| `enchantment` | 附魔 |
| `worldgen` | 世界生成 |

### Datapack Registry 格式

- Minecraft 注册表: `data/mymodid/registry_path/...`
- NeoForge/Mod 注册表: `data/mymodid/neoforge/registry_path/...`

---

## 纹理 (Textures)

### 方块纹理
```
assets/mymodid/textures/block/my_block.png
```

### 物品纹理
```
assets/mymodid/textures/item/my_item.png
```

### 建议尺寸
- 16x16 (最小)
- 32x32 (标准)
- 64x64 (高清)
- 128x128+ (超高清)

---

## 模型 (Models)

### 方块模型 (Block Model)

```json
{
    "parent": "minecraft:block/cube_all",
    "textures": {
        "all": "mymodid:block/my_block"
    }
}
```

### 物品模型 (Item Model)

```json
{
    "parent": "minecraft:item/generated",
    "textures": {
        "layer0": "mymodid:item/my_item"
    }
}
```

### 内置方块物品模型

```json
{
    "parent": "mymodid:block/my_block"
}
```

---

## 方块状态 (Blockstate)

### JSON 格式

```json
{
    "variants": {
        "facing=north,activated=false": {
            "model": "mymodid:block/my_block"
        },
        "facing=north,activated=true": {
            "model": "mymodid:block/my_block_active"
        },
        "facing=east,activated=false": {
            "model": "mymodid:block/my_block",
            "y": 90
        }
    }
}
```

### 多Part模型

```json
{
    "multipart": [
        {
            "apply": { "model": "mymodid:block/base" }
        },
        {
            "when": { "facing": "north" },
            "apply": { "model": "mymodid:block/face_north" }
        }
    ]
}
```

---

## 翻译文件

### en_us.json

```json
{
    "item.mymodid.example_item": "Example Item",
    "block.mymodid.example_block": "Example Block",
    "entity.mymodid.example_entity": "Example Entity",
    "itemGroup.mymodid.my_tab": "My Creative Tab"
}
```

### Mod 元数据翻译

```json
{
    "mod.name.examplemod": "Example Mod Name",
    "mod.description.examplemod": "This is a description"
}
```

---

## 战利品表 (Loot Tables)

### 基础掉落

```json
{
    "type": "minecraft:block",
    "pools": [
        {
            "rolls": 1,
            "entries": [
                {
                    "type": "minecraft:item",
                    "name": "mymodid:my_item"
                }
            ]
        }
    ]
}
```

### 条件掉落

```json
{
    "type": "minecraft:block",
    "pools": [
        {
            "rolls": 1,
            "entries": [
                {
                    "type": "minecraft:item",
                    "name": "minecraft:diamond"
                }
            ],
            "conditions": [
                {
                    "condition": "minecraft:survives_explosion"
                }
            ]
        }
    ]
}
```

### 工具破坏掉落

```json
{
    "type": "minecraft:block",
    "pools": [
        {
            "rolls": 1,
            "entries": [
                {
                    "type": "minecraft:item",
                    "name": "mymodid:my_item"
                }
            ],
            "conditions": [
                {
                    "condition": "minecraft:match_tool",
                    "predicate": {
                        "enchantments": [
                            {
                                "enchantment": "minecraft:silk_touch"
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```

---

## 合成配方 (Recipes)

### 形状配方

```json
{
    "type": "minecraft:crafting_shaped",
    "pattern": [
        "AAA",
        "BBB",
        "CCC"
    ],
    "key": {
        "A": { "item": "minecraft:diamond" },
        "B": { "tag": "minecraft:planks" },
        "C": { "item": "minecraft:stick" }
    },
    "result": {
        "item": "mymodid:my_item",
        "count": 2
    }
}
```

### 无序配方

```json
{
    "type": "minecraft:crafting_shapeless",
    "ingredients": [
        { "item": "minecraft:diamond" },
        { "item": "minecraft:stick" }
    ],
    "result": {
        "item": "mymodid:my_item"
    }
}
```

### 熔炉配方

```json
{
    "type": "minecraft:smelting",
    "ingredient": { "item": "mymodid:raw_ore" },
    "result": "minecraft:iron_ingot",
    "experience": 0.7,
    "cookingtime": 200
}
```

---

## 标签 (Tags)

### 方块标签

```json
{
    "replace": false,
    "values": [
        "mymodid:my_block",
        "minecraft:diamond_block",
        "#minecraft:needs_iron_tool"
    ]
}
```

### 物品标签

```json
{
    "replace": false,
    "values": [
        "mymodid:my_item",
        "#minecraft:coins"
    ]
}
```

### 常用标签

| 标签 | 说明 |
|------|------|
| `#minecraft:mineable/pickaxe` | 可用镐挖掘 |
| `#minecraft:needs_iron_tool` | 需要铁工具 |
| `#minecraft:immutable_items` | 不可变物品 |
| `#minecraft:planks` | 木板类 |

---

## 声音 (Sounds)

### sound_definitions.json

```json
{
    "mymodid:my_sound": {
        "sounds": [
            {
                "name": "mymodid:my_sound",
                "volume": 1.0,
                "pitch": 1.0
            }
        ]
    }
}
```

### 播放声音

```java
// 在世界播放
level.playSound(player, pos, SoundEvents.MY_SOUND, 
    SoundSource.BLOCKS, 1.0f, 1.0f);

// 全服播放
ServerLevel serverLevel = ...;
serverLevel.playSound(null, pos, SoundEvents.MY_SOUND,
    SoundSource.BLOCKS, 1.0f, 1.0f);
```

---

## 数据生成 (Datagen)

### 数据生成器入口

```java
@SubscribeEvent
public static void gatherData(GatherDataEvent.Client event) {
    event.createProvider(output ->
        new MyRecipeProvider(output, event.getLookupProvider())
    );
}
```

### 配方生成

```java
public class MyRecipeProvider extends RecipeProvider {
    public MyRecipeProvider(PackOutput output, 
            CompletableFuture<HolderLookup.Provider> registries) {
        super(output, registries);
    }
    
    @Override
    protected void buildRecipes(RecipeOutput output) {
        ShapedRecipeBuilder.shaped(RegistriesRecipeOutput(output), 
                MyItems.MY_ITEM.get())
            .pattern("AAA")
            .pattern("BBB")
            .define('A', Items.DIAMOND)
            .define('B', Items.STICK)
            .unlockedBy("has_diamond", has(Items.DIAMOND))
            .save(output);
    }
    
    public static class Runner extends RecipeProvider.Runner {
        public Runner(PackOutput output, 
                CompletableFuture<HolderLookup.Provider> registries) {
            super(output, registries);
        }
        
        @Override
        protected RecipeProvider createRecipeProvider(
                HolderLookup.Provider registries, RecipeOutput output) {
            return new MyRecipeProvider(output, registries);
        }
        
        @Override
        public String getName() {
            return "My Recipes";
        }
    }
}
```

### 标签生成

```java
@SubscribeEvent
public static void gatherData(GatherDataEvent.Client event) {
    event.createBlockAndItemTags(
        Registries.BLOCK,
        Registries.ITEM,
        MOD_ID,
        output -> {
            // 添加标签内容
        }
    );
}
```

---

## 注意事项

- ⚠️ 资源文件必须放置在正确路径
- ⚠️ 命名空间必须与 mod id 匹配
- ⚠️ 模型 JSON 使用小写路径
- ⚠️ 数据生成可减少手写 JSON 的错误

## 关联文档
- [NeoForge-入门.md](./NeoForge-入门.md) - 项目配置
- [NeoForge-方块.md](./NeoForge-方块.md) - 方块状态
