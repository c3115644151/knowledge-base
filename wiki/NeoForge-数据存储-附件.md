# NeoForge 数据附件系统

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/datastorage/attachments

## 概述

数据附件（Data Attachments）系统是 NeoForge 为实体等对象添加自定义数据的现代方式，相比旧版 NBT 更类型安全、更易用。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `AttachmentType<T>` | 附件类型 |
| `AttachmentHolder` | 附件持有者 |
| `RegistrationInfo` | 注册信息 |

---

## 代码示例

### 创建附件类型

```java
// 1. 简单附件
public static final AttachmentType<Integer> EXAMPLES = 
    AttachmentType.<Integer>builder(() -> 0)
        .build();

public static final AttachmentType<ItemStack> ARMOR_PIECE = 
    AttachmentType.<ItemStack>builder(() -> ItemStack.EMPTY)
        .build();

// 2. 同步到客户端
public static final AttachmentType<Integer> SYNCED_DATA = 
    AttachmentType.<Integer>builder(() -> 0)
        .sync((entity, value, dist) -> value)
        .build();

// 3. 序列化
public static final AttachmentType<CompoundTag> PERSISTENT_DATA = 
    AttachmentType.<CompoundTag>builder(CompoundTag::new)
        .serialize((entity, tag, dist) -> tag)
        .deserialize((entity, tag, dist) -> tag)
        .build();
```

### 注册附件类型

```java
// 1. 创建 DeferredRegister
private static final DeferredRegister<AttachmentType<?>> 
    ATTACHMENT_TYPES = 
    DeferredRegister.create(
        NeoForgeRegistries.Keys.ATTACHMENT_TYPES, MOD_ID);

// 2. 注册
public static final DeferredHolder<AttachmentType<?>, 
        AttachmentType<Integer>> MY_ATTACHMENT = 
    ATTACHMENT_TYPES.register("my_attachment", () -> 
        AttachmentType.<Integer>builder(() -> 0)
            .build()
    );
```

### 在实体上使用

```java
public class MyEntity extends Entity {
    // 定义附件
    @Override
    protected void defineAttachments(
            RegistrationInfo info) {
        // 使用默认值
        this.defineData(MY_ATTACHMENT, 100);
        
        // 或使用提供者
        this.defineData(MY_ATTACHMENT, 
            () -> calculateInitialValue());
    }
    
    // 获取数据
    public int getData() {
        return this.getData(MY_ATTACHMENT);
    }
    
    // 设置数据
    public void setData(int value) {
        this.setData(MY_ATTACHMENT, value);
    }
    
    // 修改数据
    public void incrementData() {
        this.setData(this.getData() + 1);
    }
}
```

### 玩家死亡复制

```java
// 默认情况下，附件数据在玩家死亡时复制到新实体
// 如需自定义行为，使用 copyOnDeath

public static final AttachmentType<Integer> COPIED_DATA = 
    AttachmentType.<Integer>builder(() -> 0)
        .copyOnDeath()
        .build();

// 自定义复制逻辑
public static final AttachmentType<CompoundTag> CUSTOM_COPY = 
    AttachmentType.<CompoundTag>builder(CompoundTag::new)
        .serialize((entity, tag, dist) -> tag)
        .deserialize((entity, tag, dist) -> tag)
        .copyOnDeath((original, clone) -> {
            // 自定义复制逻辑
            CompoundTag newTag = new CompoundTag();
            original.save(newTag);
            return newTag;
        })
        .build();
```

### 同步控制

```java
// 1. 仅服务端到客户端
public static final AttachmentType<Integer> SERVER_TO_CLIENT = 
    AttachmentType.<Integer>builder(() -> 0)
        .sync((entity, value, dist) -> {
            // 仅在 DIST.CLIENT 时同步
            return dist.isClient() ? value : null;
        })
        .build();

// 2. 双向同步
public static final AttachmentType<Integer> BIDIRECTIONAL = 
    AttachmentType.<Integer>builder(() -> 0)
        .sync((entity, value, dist) -> value)
        .build();

// 3. 不同步
public static final AttachmentType<Integer> NOT_SYNCED = 
    AttachmentType.<Integer>builder(() -> 0)
        .build();
```

---

## 注意事项

### 使用场景
- **实体数据**：替代 `SynchedEntityData`
- **持久化**：替代 NBT 存储
- **组件式数据**：更类型安全

### 常见错误
1. **数据不同步**：未正确配置 `sync` 回调
2. **默认值问题**：确保 `builder` 中提供工厂方法
3. **序列化错误**：检查 `serialize`/`deserialize` 对称性

---

## 关联引用

- 实体数据：[NeoForge-实体-数据](./NeoForge-实体-数据.md)
- 数据存储：[NeoForge-数据存储](./NeoForge-数据存储.md)
