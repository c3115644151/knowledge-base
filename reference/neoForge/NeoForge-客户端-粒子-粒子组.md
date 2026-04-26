# 客户端粒子

粒子是装饰游戏、增加沉浸感的视觉特效。由于其本质主要是视觉特性，关键部分仅存在于物理（和逻辑）[客户端][side]端。

本文涵盖粒子的渲染相关方面。关于粒子类型（通常用于生成粒子）和粒子描述（可指定粒子的精灵图）的更多信息，请参阅配套的[粒子类型][particletype]文章。

## `Particle` 类

`Particle` 定义了在世界中生成并展示给玩家的客户端表示。大多数属性和基础物理由 `gravity`、`lifetime`、`hasPhysics`、`friction` 等字段控制。唯二常被重写的方法是 `tick` 和 `move`，顾名思义各自完成其功能。因此，大多数自定义粒子通常很短，只包含一个构造函数来设置所需字段，偶尔重写这两个方法。

构建粒子的两种最常见方式是通过继承 `SingleQuadParticle` 的某个实现（如 `SimpleAnimatedParticle`）来绘制一个面向视角的纹理到屏幕；或者直接继承 `Particle`，以获得对提交渲染的[特性][features]的完全控制。

## 单个四边形

继承 `SingleQuadParticle` 的粒子会绘制一个带有某个图集精灵图的四边形到屏幕。该类提供了许多辅助方法，从设置粒子大小（通过 `quadSize` 字段或 `scale` 方法）到纹理着色（通过 `setColor` 和 `setAlpha`）。然而，四边形粒子最重要的两件事是作为纹理使用的 `TextureAtlasSprite`，以及通过 `SingleQuadParticle.Layer` 获取和渲染该精灵图的位置。

首先，`TextureAtlasSprite` 被传入构造函数，可以是自身，但更可能是 `SpriteSet`，表示其生命周期内的纹理。初始时，精灵图被设置到受保护的 `sprite` 字段，但可以在 `tick` 期间通过调用 `setSprite` 或 `setSpriteFromAge` 来更新。

:::tip
如果在粒子构造函数中更新了 `age` 或 `lifetime` 字段，应调用 `setSpriteFromAge` 来显示适当的纹理。
:::

然后，在[特性提交过程][features]中，`SingleQuadParticle.Layer` 决定使用哪个图集以及用于将四边形绘制到屏幕的管线。默认情况下，原版提供六个层级：

| 层级                   | 纹理图集        | 用途                                                    |
|:--------------------:|:-------------:|:-------------------------------------------------------|
| `OPAQUE_TERRAIN`     | 方块           | 使用无透明度的方块纹理的粒子                                  |
| `TRANSLUCENT_TERRAIN`| 方块           | 使用有透明度的方块纹理的粒子                                  |
| `OPAQUE_ITEMS`       | 物品           | 使用无透明度的物品纹理的粒子                                  |
| `TRANSLUCENT_ITEMS`  | 物品           | 使用有透明度的物品纹理的粒子                                  |
| `OPAQUE`             | 粒子           | 无透明度的粒子                                             |
| `TRANSLUCENT`        | 粒子           | 有透明度的粒子                                             |

为方便起见，如果使用原版层级之一，可以调用 `SingleQuadParticle.Layer#bySprite` 并传入纹理来确定粒子应处于哪个层级。

自定义层级可以通过调用构造函数轻松创建。

```java
public class MyQuadParticle extends SingleQuadParticle {

    public static final SingleQuadParticle.Layer EXAMPLE_LAYER = new SingleQuadParticle.Layer(
        // 粒子是否具有不完全不透明的纹理
        true,
        // 用于获取精灵图的纹理图集
        // 应与 `TextureAtlasSprite#atlasLocation` 匹配
        TextureAtlas.LOCATION_PARTICLES,
        // 用于绘制粒子的渲染管线
        // 自定义渲染管线应基于 `RenderPipelines#PARTICLE_SNIPPET`
        // 以指定可用的 uniforms 和 samplers
        RenderPipelines.WEATHER_DEPTH_WRITE
    );

    private final SpriteSet spriteSet;

    // 前四个参数不言自明
    // 精灵图集或图集精灵通常通过 provider 传入，见下文
    // 可以根据需要添加额外参数，如 xSpeed/ySpeed/zSpeed
    public MyQuadParticle(ClientLevel level, double x, double y, double z, SpriteSet spriteSet) {
        // 在构造函数中初始化精灵图集
        super(level, x, y, z, spriteSet.first());
        this.spriteSet = spriteSet;
        this.gravity = 0; // 我们的粒子现在漂浮在空中，为什么不呢
    }

    @Override
    public void tick() {
        // 让父类处理移动
        // 如有需要，可以用你自己的移动替换它
        // 如果只想修改内置移动，也可以重写 move()
        super.tick();

        // 为当前粒子年龄设置精灵图，即推进动画
        this.setSpriteFromAge(this.spriteSet);
    }

    @Override
    protected abstract SingleQuadParticle.Layer getLayer() {
        // 设置用于获取和提交纹理的层级
        return EXAMPLE_LAYER;
    }
}
```

:::warning
`SingleQuadParticle.Layer` 使用 `TextureAtlas#LOCATION_PARTICLES` 的粒子必须有关联的[粒子描述][description]。否则，粒子所需的纹理将不会被添加到图集中。
:::

## 粒子组和渲染状态

如果粒子需要比四边形更复杂的东西，则需要自己的 `ParticleGroup<P>`，其中 `P` 是 `Particle` 的类型。`ParticleGroup` 负责驱动一组定义的 `Particle` 子集，并在 `Particle#isAlive` 返回 false 时将其移除。每个组最多可队列 16,384 个粒子，满时驱逐最旧的。

```java
// 假设我们有以下粒子类
public class ComplexParticle extends Particle {

    // 不强制使用这些字段或存储这些值
    // 由你决定要渲染什么以及获取适当的数据
    private final Model.Simple model;
    private final SpriteId sprite;

    public ComplexParticle(ClientLevel level, double x, double y, double z) {
        super(level, x, y, z);
        this.model = StandingSignRenderer.createSignModel(
            Minecraft.getInstance().getEntityModels(), WoodType.OAK, PlainSignBlock.Attachment.GROUND
        );
        this.sprite = Sheets.getSignSprite(WoodType.OAK);
    }

    public Model.Simple model() {
        return this.model;
    }

    public SpriteId sprite() {
        return this.sprite;
    }
}

// 我们可以像这样创建一个基本的粒子组
public class ComplexParticleGroup extends ParticleGroup<ComplexParticle> {

    public ComplexParticleGroup(ParticleEngine engine) {
        super(engine);
    }

    // ...
}
```

一旦 `Particle` 被添加到 `ParticleGroup`，它会在[特性提交][features]期间通过 `ParticleGroup#extractRenderState` 被提取到 `ParticleGroupRenderState`。`ParticleGroupRenderState` 是包含提取粒子的渲染状态和用于提交粒子元素进行渲染的处理程序（通过 `#submit`）的混合体。

```java
// 粒子组渲染状态
public record ComplexParticleRenderState(List<ComplexParticleRenderState.Entry> entries) implements ParticleGroupRenderState {

    // 每个条目代表组中的一个粒子
    public record Entry(Model.Simple model, SpriteId sprite, PoseStack pose) {}

    @Override
    public void submit(SubmitNodeCollector collector, CameraRenderState camera) {
        // 提交粒子元素进行渲染
        for (ComplexParticleRenderState.Entry entry : this.entries) {
            collector.submitModel(...);
        }
    }
}

// 在组中...
public class ComplexParticleGroup extends ParticleGroup<ComplexParticle> {

    // ...

    @Override
    public ParticleGroupRenderState extractRenderState(Frustum frustum, Camera camera, float partialTickTime) {
        // 从粒子中提取渲染状态
        List<ComplexParticleRenderState.Entry> entries = new ArrayList<>();

        for (ComplexParticle particle : this.particles) {
            PoseStack pose = new PoseStack();
            pose.pushPose();
            pose.mulPose(camera.rotation());
            entries.add(new ComplexParticleRenderState.Entry(particle.model(), particle.sprite(), pose));
        }

        return new ComplexParticleRenderState(entries);
    }
}
```

单独来看，`Particle` 不知道它属于哪个 `ParticleGroup`，`ParticleEngine` 也不知道该组的存在。这些都是使用 `ParticleRenderType` 链接在一起的：`ParticleRenderType` 是该组的唯一标识符。`ParticleRenderType` 通过[客户端][side] [mod bus][modbus] [事件][event] `RegisterParticleGroupsEvent` 链接到 `ParticleGroup`。然后，`Particle` 可以通过将 `Particle#getGroup` 设置为创建的 `ParticleRenderType` 来使用该组。

```java
// 创建渲染类型
// 传入的字符串应该是字符串化的 `Identifier`
public static final ParticleRenderType COMPLEX = new ParticleRenderType("examplemod:complex");

@SubscribeEvent // 仅在物理客户端的 mod event bus 上
public static void registerParticleProviders(RegisterParticleGroupsEvent event) {
    // 将渲染类型链接到粒子组
    event.register(COMPLEX, ComplexParticleGroup::new);
}

public class ComplexParticle extends Particle {

    // ...

    @Override
    public ParticleRenderType getGroup() {
        // 告诉粒子使用粒子组进行渲染
        return COMPLEX;
    }
}
```

## `ParticleProvider`

一旦为某个粒子类型创建了粒子，该粒子类型必须通过 `ParticleProvider` 链接。`ParticleProvider` 是一个仅限客户端的类，负责通过 `createParticle` 从 `ParticleEngine` 实际创建我们的 `Particle`。虽然这里可以包含更复杂的代码，但许多粒子提供者就像这样简单：

```java
// ParticleProvider 的泛型类型必须与此 provider 所服务的粒子类型匹配
public class MyQuadParticleProvider implements ParticleProvider<SimpleParticleType> {

    // 一组粒子精灵图
    private final SpriteSet spriteSet;

    // 注册函数传入一个 SpriteSet，所以我们接受它并存储以供进一步使用
    // 如果你的粒子不需要 SpriteSet，可以省略此构造函数
    public MyParticleProvider(SpriteSet spriteSet) {
        this.spriteSet = spriteSet;
    }

    // 魔法发生的地方。每次调用此方法时我们都返回一个新粒子！
    // 第一个参数的类型与传递给超接口的泛型类型匹配
    @Override
    @Nullable
    public Particle createParticle(SimpleParticleType particleType, ClientLevel level, double x, double y, double z, double xd, double yd, double zd, RandomSource random
    ) {
        // 我们不使用类型、速度增量或引擎随机数
        return new MyQuadParticle(level, x, y, z, this.spriteSet);
    }
}
```

然后，你的粒子提供者必须在[客户端][side] [mod bus][modbus] [事件][event] `RegisterParticleProvidersEvent` 中与粒子类型关联：

```java
@SubscribeEvent // 仅在物理客户端的 mod event bus 上
public static void registerParticleProviders(RegisterParticleProvidersEvent event) {
    // 有多种方式注册 provider，都取决于第二个参数提供的函数类型
    // 例如，#registerSpriteSet 代表 Function<SpriteSet, ParticleProvider<?>>：
    event.registerSpriteSet(MyParticleTypes.MY_QUAD_PARTICLE.get(), MyQuadParticleProvider::new);

    // 另一方面，#registerSpecial 映射到 ParticleProvider<?>
    // 如果精灵图不是从粒子描述获取的，应使用此方法
}
```

:::warning
如果使用 `registerSpriteSet`，则粒子类型还必须有关联的[粒子描述][description]。否则，将抛出异常，说明 'Failed to load description'。
:::

[description]: ../resources/client/particles.md
[event]: ../concepts/events.md
[features]: feature.md
[modbus]: ../concepts/events.md#event-buses
[particletype]: ../resources/client/particles.md
[registry]: ../concepts/registries.md#methods-for-registering
[side]: ../concepts/sides.md
