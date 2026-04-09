# NeoForge 粒子系统

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/client/particles

## 概述

粒子系统用于创建各种视觉特效，如烟雾、火焰、魔法光效等。每个粒子类型都有特定的生成和渲染方式。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `ParticleType<T>` | 粒子类型基类 |
| `ParticleOptions` | 粒子选项接口 |
| `ParticleRenderType` | 粒子渲染类型 |
| `ParticleProvider` | 粒子提供者 |

---

## 代码示例

### 创建粒子类型

```java
// 1. 定义粒子选项
public class CustomParticleOptions implements ParticleOptions {
    private final float red;
    private final float green;
    private final float blue;
    
    public CustomParticleOptions(float red, 
            float green, float blue) {
        this.red = red;
        this.green = green;
        this.blue = blue;
    }
    
    public float getRed() { return red; }
    public float getGreen() { return green; }
    public float getBlue() { return blue; }
    
    @Override
    public ParticleType<CustomParticleOptions> getType() {
        return ModParticles.CUSTOM_PARTICLE.get();
    }
    
    // 工厂方法
    public static DeserializationContextDeserializer<CustomParticleOptions>
        CONTEXT_DESERIALIZER = (deserializer, 
            compoundTag, deserializationContext) -> {
        return new CustomParticleOptions(
            compoundTag.getFloat("r"),
            compoundTag.getFloat("g"),
            compoundTag.getFloat("b")
        );
    };
}

// 2. 注册粒子类型
private static final DeferredRegister<ParticleType<?>> PARTICLES = 
    DeferredRegister.create(
        NeoForgeRegistries.Keys.PARTICLE_TYPES, MOD_ID);

public static final DeferredHolder<ParticleType<?>, 
        ParticleType<CustomParticleOptions>> CUSTOM_PARTICLE = 
    PARTICLES.register("custom_particle", () -> 
        new ParticleType<CustomParticleOptions>(
            false,  // 始终显示
            CustomParticleOptions.CONTEXT_DESERIALIZER
        ) {
            @Override
            public Codec<CustomParticleOptions> codec() {
                return RecordCodecBuilder.create(instance ->
                    instance.group(
                        Codec.FLOAT.fieldOf("r").forGetter(
                            CustomParticleOptions::getRed),
                        Codec.FLOAT.fieldOf("g").forGetter(
                            CustomParticleOptions::getGreen),
                        Codec.FLOAT.fieldOf("b").forGetter(
                            CustomParticleOptions::getBlue)
                    ).apply(instance, CustomParticleOptions::new)
                );
            }
        }
    );
```

### 创建粒子渲染器

```java
// 1. 实现粒子提供者
public class CustomParticleProvider 
        implements ParticleProvider<CustomParticleOptions> {
    
    private final SpriteSet spriteSet;
    
    public CustomParticleProvider(SpriteSet spriteSet) {
        this.spriteSet = spriteSet;
    }
    
    @Override
    public Particle createParticle(
            CustomParticleOptions data,
            ClientLevel level,
            double x, double y, double z,
            double xSpeed, double ySpeed, double zSpeed) {
        
        // 创建粒子
        ColoredParticle particle = new ColoredParticle(
            level, x, y, z,
            xSpeed, ySpeed, zSpeed,
            data.getRed(), data.getGreen(), data.getBlue(),
            this.spriteSet
        );
        
        // 设置生命周期等
        particle.setLifetime(60);  // 60 ticks
        particle.setSize(0.1f, 0.1f);
        
        return particle;
    }
}

// 2. 创建粒子类
public class ColoredParticle extends TextureSheetParticle {
    private final float rCol, gCol, bCol;
    
    public ColoredParticle(ClientLevel level,
            double x, double y, double z,
            double xSpeed, double ySpeed, double zSpeed,
            float r, float g, float b,
            SpriteSet sprite) {
        super(level, x, y, z, xSpeed, ySpeed, zSpeed);
        this.rCol = r;
        this.gCol = g;
        this.bCol = b;
        this.setSprite(sprite.get(
            level.random.nextFloat(),
            level.random.nextFloat()
        ));
        this.quadSize = 0.1f;
        this.lifetime = 60;
    }
    
    @Override
    protected int getLightColor(float partialTick) {
        return 0xF000F0;  // 明亮
    }
    
    @Override
    public ParticleRenderType getRenderType() {
        return ParticleRenderType.PARTICLE_SHEET_OPAQUE;
    }
    
    @Override
    public void tick() {
        super.tick();
        // 渐变消失
        this.alpha = (float) this.lifetime / 60.0f;
    }
}

// 3. 注册提供者
@Mod.EventBusSubscriber(modid = MOD_ID, 
    bus = Mod.EventBusSubscriber.Bus.MOD, 
    value = Dist.CLIENT)
public static class ClientSetup {
    @SubscribeEvent
    public static void registerParticleFactories(
            RegisterParticleProviderEvent event) {
        event.registerSpriteSet(
            ModParticles.CUSTOM_PARTICLE.get(),
            CustomParticleProvider::new
        );
    }
}
```

### 生成粒子

```java
// 1. 在世界中生成
public static void spawnParticles(Level level, 
        Vec3 position) {
    
    // 基础生成
    level.addParticle(
        ModParticles.CUSTOM_PARTICLE.get()
            .createParticle(
                new CustomParticleOptions(1.0f, 0.0f, 0.0f),
                level,
                position.x, position.y, position.z,
                0, 0.1, 0  // 速度
            )
    );
    
    // 生成多个
    for (int i = 0; i < 10; i++) {
        level.addParticle(
            new CustomParticleOptions(
                level.random.nextFloat(),
                level.random.nextFloat(),
                level.random.nextFloat()
            ),
            position.x + (level.random.nextDouble() - 0.5),
            position.y + level.random.nextDouble(),
            position.z + (level.random.nextDouble() - 0.5),
            0, 0.05, 0
        );
    }
}

// 2. 在实体上生成
public void spawnFromEntity(LivingEntity entity) {
    level.addParticle(
        new CustomParticleOptions(0, 1, 1),
        entity.getX(),
        entity.getY() + entity.getBbHeight(),
        entity.getZ(),
        entity.getViewYRot(0),
        0.2,
        0
    );
}

// 3. 使用 ParticleOptions 广泛生成
public static void spawnParticleBurst(Level level, 
        Vec3 center, int count) {
    ParticleOptions options = new CustomParticleOptions(
        1.0f, 1.0f, 1.0f);
    
    level.sendParticles(
        options,
        center.x, center.y, center.z,
        count,
        0.5, 0.5, 0.5,  // 扩散范围
        0.01             // 速度偏移
    );
}

// 4. 玩家可见的粒子
public static void spawnForPlayer(Level level, Vec3 pos, 
        Player player) {
    level.sendParticles(
        player,
        new CustomParticleOptions(0, 1, 0),
        pos.x, pos.y, pos.z,
        1, 0, 0, 0, 0
    );
}
```

### 粒子描述文件

```json
// assets/<namespace>/particles/<particle_name>.json
{
    "textures": [
        "examplemod:particle/spark_0",
        "examplemod:particle/spark_1",
        "examplemod:particle/spark_2",
        "examplemod:particle/spark_3"
    ]
}
```

---

## 内置粒子类型

| 类型 | 描述 |
|------|------|
| `AMBIENT_ENTITY_EFFECT` | 环境实体效果（药水云） |
| `ANGRY_VILLAGER` | 愤怒村民 |
| `BLOCK` | 方块碎片 |
| `BUBBLE` | 气泡 |
| `CLOUD` | 云 |
| `CRIT` | 暴击 |
| `DAMAGE_INDICATOR` | 伤害指示器 |
| `DRAGON_BREATH` | 龙息 |
| `DRIPPING_LAVA` | 滴水熔岩 |
| `DUST` | 彩色粉尘 |
| `EFFECT` | 效果 |
| `ELDER_GUARDIAN` | 老守卫者 |
| `ENCHANTED_HIT` | 附魔打击 |
| `ENCHANT` | 附魔 |
| `END_ROD` | 末影棒 |
| `ENTITY_EFFECT` | 实体效果 |
| `EXPLOSION` | 爆炸 |
| `FALLING_DUST` | 落尘 |
| `FIREWORK` | 烟花 |
| `FLAME` | 火焰 |
| `FLASH` | 闪光 |
| `GREAT_WHITE_SHARK` | 大白鲨 |
| `GUST` | 阵风 |
| `GUST_DUST` | 阵风尘埃 |
| `HAPPY_VILLAGER` | 快乐村民 |
| `HEART` | 心形 |
| `INSTANT_EFFECT` | 即时效果 |
| `ITEM` | 物品 |
| `LAYER` | 层 |
| `LEGACY_BLOCK` | 遗留方块 |
| `LIGHT` | 亮光 |
| `MAELSTROM` | 漩涡 |
| `NOTE` | 音符 |
| `PARTICLE` | 通用粒子 |
| `POOF` | 暴击 |
| `PORTAL` | 传送门 |
| `RAIN` | 雨滴 |
| `SCULK_CHARGE` | 幽匿充能 |
| `SCULK_CHARGE_POOF` | 幽匿充能爆炸 |
| `SCULK_SOUL` | 幽匿灵魂 |
| `SHRIEK` | 尖啸 |
| `SLIME` | 史莱姆 |
| `SMALL_FLAME` | 小火焰 |
| `SMOKE` | 烟雾 |
| `SNEEZE` | 喷嚏 |
| `SNOWFLAKE` | 雪花 |
| `SOUL` | 灵魂 |
| `SOUL_FIRE_FLAME` | 灵魂火焰 |
| `SPARK` | 火花 |
| `SPAWN` | 生成 |
| `SPIT` | 吐息 |
| `SQUIRT` | 喷射 |
| `TRIAL_OMEN` | 审判预兆 |
| `VIBRATION` | 振动 |
| `WATER` | 水滴 |
| `WAX_OFF` | 蜂蜡移除 |
| `WAX_ON` | 蜂蜡添加 |
| `WHITE_SMOKE` | 白烟 |
| `WITHER_BOSS` | 凋灵Boss |
| `WITHER_INSTANT` | 凋灵即时 |

---

## 注意事项

### 性能考虑
- 避免大量生成同种粒子
- 使用 `setSize` 控制粒子大小
- 合理设置 `lifetime`

### 常见错误
1. **粒子不显示**：检查粒子类型注册和提供者
2. **纹理缺失**：确保纹理文件存在
3. **客户端/服务端混淆**：粒子生成代码需在客户端

### 最佳实践

```java
// 推荐：使用 SpriteSet
public class ParticleFactory {
    public ParticleProvider<CustomParticleOptions> create(
            SpriteSet sprites) {
        return (data, level, x, y, z, xs, ys, zs) -> {
            ColoredParticle particle = 
                new ColoredParticle(level, x, y, z, 
                    xs, ys, zs, sprites);
            particle.pickSprite(sprites);
            return particle;
        };
    }
}
```

---

## 关联引用

- 客户端基础：[NeoForge-客户端基础](./NeoForge-客户端基础.md)
- 纹理：[NeoForge-客户端-纹理](./NeoForge-客户端-纹理.md)
- 渲染：[NeoForge-渲染-特性](./NeoForge-渲染-特性.md)
