# NeoForge 实体开发

## 注册实体

### EntityType 注册

```java
public static final DeferredRegister.Entities ENTITY_TYPES =
    DeferredRegister.createEntities(MOD_ID);

public static final Supplier<EntityType<MyEntity>> MY_ENTITY = 
    ENTITY_TYPES.register(
        "my_entity",
        () -> EntityType.Builder.of(
            MyEntity::new,           // 工厂方法
            MobCategory.MISC        // 实体分类
        )
        .sized(1.0f, 1.0f)         // 宽高
        .clientTrackingRange(8)     // 客户端追踪范围
        .updateInterval(10)        // 更新间隔
        .noSummon()                // 禁用/summon
        .noSave()                  // 不保存到磁盘
        .fireImmune()              // 火焰免疫
        .build(ResourceKey.create(
            Registries.ENTITY_TYPE,
            Identifier.fromNamespaceAndPath(MOD_ID, "my_entity")
        ))
    );
```

### MobCategory 分类

| 分类 | 刷怪上限 | 示例 |
|------|----------|------|
| `MONSTER` | 70 | 僵尸、骷髅 |
| `CREATURE` | 10 | 动物 |
| `AMBIENT` | 15 | 蝙蝠 |
| `AXOLOTLS` | 5 | 美西螈 |
| `WATER_CREATURE` | 5 | 鱿鱼、海豚 |
| `WATER_AMBIENT` | 20 | 鱼 |
| `UNDERGROUND_WATER_CREATURE` | 5 | 发光鱿鱼 |
| `MISC` | 无 | 投射物 |

⚠️ `MobCategory` 是可扩展枚举，可添加自定义分类

---

## 实体类

### 基本结构

```java
public class MyEntity extends Entity {
    public MyEntity(EntityType<?> type, Level level) {
        super(type, level);
    }
    
    @Override
    protected void readAdditionalSaveData(ValueInput input) {
        // 读取存档数据
    }
    
    @Override
    protected void addAdditionalSaveData(ValueOutput output) {
        // 保存存档数据
    }
    
    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        // 定义同步数据
    }
    
    @Override
    public boolean hurtServer(
            ServerLevel level, 
            DamageSource source, 
            float amount) {
        return true;
    }
}
```

### 数据同步

```java
// 定义同步数据
@Override
protected void defineSynchedData(SynchedEntityData.Builder builder) {
    builder.define(DATA_ID, 0);
}

// 使用
private static final EntityDataAccessor<Integer> DATA_ID = 
    SynchedEntityData.defineId(MyEntity.class, VarInt策.codec());

// 读取
int value = entityData.get(DATA_ID);

// 设置（仅服务端）
this.entityData.set(DATA_ID, newValue);
this.entityData.setDirty(DATA_ID, true);
```

### 存档数据

```java
@Override
protected void readAdditionalSaveData(ValueInput input) {
    this.value = input.getIntOr("value", 0);
}

@Override
protected void addAdditionalSaveData(ValueOutput output) {
    output.putInt("value", this.value);
}
```

---

## 实体生成

### 代码生成

```java
// 服务端生成
if (!level.isClientSide()) {
    MyEntity entity = new MyEntity(
        MY_ENTITY.get(), level, x, y, z
    );
    level.addFreshEntity(entity);
}

// 使用 EntityType 生成
MY_ENTITY.get().spawn(
    serverLevel,        // ServerLevel
    null,               // 额外数据 (可null)
    null,               // 生成消费者 (可null)
    pos,                // 生成位置
    MobSpawnType.COMMAND, // 生成类型
    true,               // 是否不生成（检查位置）
    true                // 是否在最近位置生成
);
```

### 生成类型 (MobSpawnType)

| 类型 | 说明 |
|------|------|
| `NATURAL` | 自然生成 |
| `MOB_SUMMONED` | 刷怪笼 |
| `COMMAND` | /summon 命令 |
| `DISPENSER` | 发射器 |
| `SPAWNER` | 刷怪器 |
| `EVENT` | 事件触发 |

---

## 实体伤害

```java
// 造成伤害
entity.hurt(entity.damageSources().wither(), 4.0f);
// 或
entity.hurtOrSimulate(entity.damageSources().wither(), 4.0f);

// 自定义伤害处理
@Override
public boolean hurtServer(
        ServerLevel level, 
        DamageSource source, 
        float amount) {
    if (source.is(DamageTypeTags.IS_FIRE)) {
        return super.hurtServer(level, source, amount * 2);
    }
    return false;
}

// Difference: hurt() 只在服务端执行，hurtOrSimulate() 两端都执行
```

---

## Ticking

```java
@Override
public void tick() {
    super.tick();
    
    // 每tick执行
    if (this.tickCount % 5 == 0) {
        // 每5tick执行
    }
}

// 其他tick方法
// baseTick() - 更新基础状态（燃烧、冻结、游泳、传送门）
// rideTick() - 骑乘时的tick
```

---

## 实体分类层级

```
Entity
├── Projectile（投射物）
│   ├── AbstractArrow（箭矢）
│   ├── ThrowableProjectile（可抛物品）
│   └── AbstractHurtingProjectile（伤害投射物）
├── LivingEntity（生物）
│   ├── Mob（怪物）
│   └── Player（玩家）
├── VehicleEntity（载具）
│   ├── AbstractBoat
│   └── AbstractMinecart
├── BlockAttachedEntity
│   ├── ItemFrame
│   └── LeashFenceKnotEntity
└── PartEntity（多部分实体）
```

---

## 投射物

### 自定义投射物

```java
public class MyProjectile extends Projectile {
    public MyProjectile(
            EntityType<? extends Projectile> type, 
            Level level) {
        super(type, level);
    }
    
    @Override
    protected void onHit(HitResult result) {
        // 命中处理
        if (result.getType() == EntityType.ENTITY) {
            // 命中实体
        } else if (result.getType() == BlockType.BLOCK) {
            // 命中方块
        }
        super.onHit(result);
    }
    
    // 发射
    public void shoot(double x, double y, double z, float velocity, float divergence) {
        Vec3 vec = new Vec3(x, y, z).normalize().scale(velocity);
        this.setDeltaMovement(vec);
        // ...
    }
}
```

### 常见方法

| 方法 | 说明 |
|------|------|
| `shoot()` | 设置速度和方向 |
| `onHit()` | 命中回调 |
| `onHitEntity()` | 命中实体 |
| `onHitBlock()` | 命中方块 |
| `getOwner()` | 获取发射者 |
| `setOwner()` | 设置发射者 |
| `deflect()` | 偏转投射物 |

---

## 实体附件 (Entity Attachments)

### 用于定义实体上的视觉挂载点

```java
// 定义在 EntityType.Builder 中
EntityType.Builder.of(...)
    .attach(EntityAttachment.NAME_TAG, 0, 0.5f, 0)  // 名称标签偏移
    .passengerAttachment(Vec3.ZERO)                  // 乘客挂载点
    .vehicleAttachment(Vec3.ZERO)                    // 载具挂载点
```

### 附件类型

| 附件 | 默认位置 | 用途 |
|------|----------|------|
| `PASSENGER` | 碰撞箱中心 | 骑乘者位置 |
| `VEHICLE` | 碰撞箱底部中心 | 被骑乘时位置 |
| `NAME_TAG` | 碰撞箱顶部中心 | 名称标签 |
| `WARDEN_CHEST` | 碰撞箱中心 | 音波攻击起点 |

---

## 拾取物品结果

```java
@Override
@Nullable
public ItemStack getPickResult() {
    return new ItemStack(MyItems.MY_SPAWN_EGG.get());
}

// 禁用拾取
@Override
public boolean isPickable() {
    return false;
}
```

---

## 常见问题

### 何时使用 Entity vs LivingEntity？

| Entity | LivingEntity |
|--------|--------------|
| 基础实体 | 有生命值的实体 |
| 投射物 | 怪物、动物、玩家 |
| 无装备栏 | 有装备栏 |
| 无药水效果 | 有药水效果 |

### 注意事项

- ❌ 实体逻辑必须在服务端执行
- ❌ 不要在实体类中直接使用静态字段
- ❌ 创建多个实体部件时使用 PartEntity

## 关联文档
- [NeoForge-概念.md](./NeoForge-概念.md) - 事件与注册表
- [NeoForge-网络.md](./NeoForge-网络.md) - 实体数据同步
