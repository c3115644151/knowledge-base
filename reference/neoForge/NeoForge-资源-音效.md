# NeoForge 资源 - 音效

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/client/sounds

## 术语

| 术语 | 说明 |
|------|------|
| Sound Event | 代码中的触发器，告诉音效引擎播放特定音效 |
| Sound Source | 音效分类，用于在设置中单独调节 |
| Sound Definition | 音效事件到一个或多个音效对象的映射 |
| Sound Object | 包含音效文件位置和可选元数据的 JSON 对象 |
| Sound File | 磁盘上的音效文件，Minecraft 仅支持 `.ogg` 格式 |

> ⚠️ **注意**：由于 OpenAL 实现，音效文件必须为单声道（单通道）才能有衰减效果。立体声文件不会根据距离衰减。

## 考古音效（原版 SoundEvents）

> ⚠️ **1.21 版本命名规范**：Moja ng 官方映射在 1.21 中移除了冗余前缀，
> `ITEM_BRUSH_BRUSHING_GENERIC` → `BRUSH_GENERIC`，不得使用旧版名称。

### 刷取音效（SoundEvents）

| 描述 | 1.21 官方字段名 | 旧版名称（已废弃） |
|------|----------------|------------------|
| 刷取通用方块 | `SoundEvents.BRUSH_GENERIC` | `ITEM_BRUSH_BRUSHING_GENERIC` |
| 刷取可疑砂砾 | `SoundEvents.BRUSH_GRAVEL` | `ITEM_BRUSH_BRUSHING_GRAVEL` |
| 刷取可疑沙子 | `SoundEvents.BRUSH_SAND` | `ITEM_BRUSH_BRUSHING_SAND` |
| 刷取完成（砂砾） | `SoundEvents.BRUSH_GRAVEL_COMPLETED` | - |
| 刷取完成（沙子） | `SoundEvents.BRUSH_SAND_COMPLETED` | - |

**注意**：不存在 `BRUSH_GENERIC_COMPLETED` 或 `BRUSH_COMPLETED` 等字段。
`BrushableBlock` 构造函数第二个参数为刷取中音效，第三个参数为完成音效。

### 注册自定义 SoundEvent

`SoundEvent` 是注册对象，必须通过 `DeferredRegister` 注册：

```java
public class MySoundsClass {
    public static final DeferredRegister<SoundEvent> SOUND_EVENTS =
            DeferredRegister.create(BuiltInRegistries.SOUND_EVENT, "examplemod");

    public static final Holder<SoundEvent> MY_SOUND = SOUND_EVENTS.register(
            "my_sound",
            SoundEvent::createVariableRangeEvent
    );

    public static final Holder<SoundEvent> MY_FIXED_SOUND = SOUND_EVENTS.register(
            "my_fixed_sound",
            registryName -> SoundEvent.createFixedRangeEvent(registryName, 16f)
    );
}
```

在 mod 构造函数中注册：

```java
public ExampleMod(IEventBus modBus) {
    MySoundsClass.SOUND_EVENTS.register(modBus);
}
```

## sounds.json

连接 SoundEvent 到实际音效文件，创建命名空间根目录的 `sounds.json`：

```json
{
    "my_sound": {
        "sounds": [
            {
                "name": "examplemod:sound_1",
                "type": "sound",
                "volume": 0.8,
                "pitch": 1.1,
                "weight": 3,
                "stream": true,
                "attenuation_distance": 8,
                "preload": true
            },
            "examplemod:sound_2"
        ]
    },
    "my_fixed_sound": {
        "replace": true,
        "subtitle": "examplemod.my_fixed_sound",
        "sounds": ["examplemod:sound_1", "examplemod:sound_2"]
    }
}
```

### 音效对象字段

| 字段 | 说明 |
|------|------|
| `name` | 音效文件位置 |
| `type` | `"sound"` 或 `"event"` |
| `volume` | 音量，0.0-1.0 |
| `pitch` | 音高，0.0-2.0 |
| `weight` | 从列表中选择时的权重 |
| `stream` | 是否流式播放（适合长音效） |
| `attenuation_distance` | 衰减距离覆盖 |
| `preload` | 是否预加载到内存 |

### sounds.json 合并

`sounds.json` 不覆盖，而是合并。`replace: true` 替换，`replace: false` 添加。

## 播放音效

### Level 方法

```java
// 播放音效（自动处理客户端/服务端）
level.playSeededSound(entity, x, y, z, soundEvent, soundSource, volume, pitch, seed);
level.playSound(entity, x, y, z, soundEvent, soundSource, volume, pitch);

// 本地播放（仅客户端）
level.playLocalSound(x, y, z, soundEvent, soundSource, volume, pitch, distanceDelay);

// 基于玩家位置播放
level.playPlayerSound(soundEvent, soundSource, volume, pitch);
```

### Entity 方法

```java
entity.playSound(soundEvent, volume, pitch);
```

### Player 方法

```java
player.playSound(soundEvent, volume, pitch);
```

## SoundSource 枚举

| 来源 | 说明 |
|------|------|
| MASTER | 主音量 |
| MUSIC | 背景音乐 |
| RECORDS | 红石唱片/音符盒 |
| WEATHER | 天气音效 |
| BLOCKS | 方块交互音效 |
| HOSTILE | 敌对生物音效 |
| NEUTRAL | 中立生物音效 |
| PLAYERS | 玩家音效 |
| AMBIENT | 环境音效 |
| VOICE | 语音（很少使用） |

## 数据生成

```java
public class MySoundDefinitionsProvider extends SoundDefinitionsProvider {
    public MySoundDefinitionsProvider(PackOutput output) {
        super(output, "examplemod");
    }

    @Override
    public void registerSounds() {
        add(MySoundsClass.MY_SOUND, SoundDefinition.definition()
            .with(
                sound("examplemod:sound_1", SoundDefinition.SoundType.SOUND)
                    .volume(0.8f)
                    .pitch(1.2f)
                    .weight(2)
                    .attenuationDistance(8)
                    .stream(true)
                    .preload(true),
                sound("examplemod:sound_2")
            )
            .subtitle("sound.examplemod.sound_1")
            .replace(true)
        );
    }
}

@SubscribeEvent
public static void gatherData(GatherDataEvent.Client event) {
    event.createProvider(MySoundDefinitionsProvider::new);
}
```

## 关联引用

- [纹理](./NeoForge-资源-纹理.md)
- [模型](./NeoForge-资源-模型.md)
