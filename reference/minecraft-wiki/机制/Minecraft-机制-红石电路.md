# Minecraft 机制：红石电路 (Redstone Circuits)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/红石电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

红石对模组开发的核心价值不是“玩家怎么搭电路”，而是“你如何让自定义方块正确参与信号网络”。大部分红石兼容性问题都来自：信号输出/输入接口不完整、邻居更新不正确、客户端表现与服务端逻辑不一致。

### NeoForge 对照文档

- [NeoForge 方块开发](../../neoForge/NeoForge-方块.md)
- [NeoForge-方块-状态](../../neoForge/NeoForge-方块-状态.md)

### 1. 方块的信号接口（你自定义红石行为的最小集合）
常见需要明确实现/覆写的方法（名称以 Mojang 映射为参照）：
- `isSignalSource(BlockState)`：该方块是否能输出红石信号
- `getSignal(BlockState, BlockGetter, BlockPos, Direction)`：弱红石信号强度（0–15）
- `getDirectSignal(BlockState, BlockGetter, BlockPos, Direction)`：强红石信号（某些方块/场景会用到）
- `hasAnalogOutputSignal(BlockState)` 与 `getAnalogOutputSignal(BlockState, Level, BlockPos)`：比较器输出（容器/状态方块常用）

你需要先决定“你的方块像什么”：
- 像按钮/拉杆：输出脉冲/保持信号，通常需要状态切换 + 定时复位
- 像红石块：持续强信号源
- 像容器：提供比较器信号（模拟信号）

### 2. 更新机制：neighborChanged / scheduledTick / block updates
红石系统对“更新传播”非常敏感。常见坑：
- 状态改变了，但没有通知邻居（信号不刷新）
- 过度通知导致卡顿（尤其是大规模红石/自动化场景）
- 逻辑在客户端执行导致不同步（红石必须以服务端为权威）

实现时通常会用到：
- `neighborChanged(...)`：邻居变化时重新计算本方块状态
- `onPlace(...)` / `onRemove(...)`：放置/移除时触发周边刷新
- `tick(...)`（计划刻）/ `scheduleTick(...)`：用于延迟更新、脉冲长度控制、去抖动

### 3. 信号强度与衰减（与比较器/中继器联动）
- 绝大多数红石信号强度为 0–15。
- 红石粉每格衰减 1；中继器可恢复到 15；比较器可保持/计算模拟强度。
- 如果你的方块输出模拟值（如进度、能量、库存），优先通过比较器接口暴露。

### 4. Java/基岩差异（只保留会影响实现的点）
Wiki 中红石的大量内容属于“电路学”。模组实现层面更重要的是：
- Java 版很多红石行为依赖“方块更新”传播链（block updates）
- 部分特性（例如半连接 QC）属于 Java 版特性，会影响活塞/发射器等交互

---

## 原版 Wiki 快速索引 (Quick Reference)

红石条目极长，本地不复述，保留精确锚点入口。

### 基本概念（建议先读完这一组再做红石兼容方块）
- [基本概念](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5)
- [红石元件](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E7%BA%A2%E7%9F%B3%E5%85%83%E4%BB%B6)
- [信号与脉冲](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E4%BF%A1%E5%8F%B7%E4%B8%8E%E8%84%89%E5%86%B2)
- [信号强度](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E4%BF%A1%E5%8F%B7%E5%BC%BA%E5%BA%A6)
- [激活](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E6%BF%80%E6%B4%BB)
- [充能](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%85%85%E8%83%BD)
- [充能与激活的不同](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%85%85%E8%83%BD%E4%B8%8E%E6%BF%80%E6%B4%BB%E7%9A%84%E4%B8%8D%E5%90%8C)

### 更新与底层机制（对模组最关键的一节）
- [方块更新（狭义）](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E6%96%B9%E5%9D%97%E6%9B%B4%E6%96%B0%EF%BC%88%E7%8B%AD%E4%B9%89%EF%BC%89)
- [红石刻](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E7%BA%A2%E7%9F%B3%E5%88%BB)

---

### Wiki 全目录（H2/H3/H4）

- [基本概念](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5)
  - [红石元件](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E7%BA%A2%E7%9F%B3%E5%85%83%E4%BB%B6)
  - [位置](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E4%BD%8D%E7%BD%AE)
  - [电路与机械](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E7%94%B5%E8%B7%AF%E4%B8%8E%E6%9C%BA%E6%A2%B0)
  - [信号与脉冲](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E4%BF%A1%E5%8F%B7%E4%B8%8E%E8%84%89%E5%86%B2)
    - [边沿](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E8%BE%B9%E6%B2%BF)
    - [相位](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E7%9B%B8%E4%BD%8D)
    - [脉冲](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E8%84%89%E5%86%B2)
  - [信号强度](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E4%BF%A1%E5%8F%B7%E5%BC%BA%E5%BA%A6)
  - [激活](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E6%BF%80%E6%B4%BB)
  - [充能](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%85%85%E8%83%BD)
    - [充能类型](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%85%85%E8%83%BD%E7%B1%BB%E5%9E%8B)
    - [充能等级](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%85%85%E8%83%BD%E7%AD%89%E7%BA%A7)
  - [充能与激活的不同](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%85%85%E8%83%BD%E4%B8%8E%E6%BF%80%E6%B4%BB%E7%9A%84%E4%B8%8D%E5%90%8C)
  - [方块更新（狭义）](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E6%96%B9%E5%9D%97%E6%9B%B4%E6%96%B0%EF%BC%88%E7%8B%AD%E4%B9%89%EF%BC%89)
  - [红石系统](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E7%BA%A2%E7%9F%B3%E7%B3%BB%E7%BB%9F)
    - [部分细节](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E9%83%A8%E5%88%86%E7%BB%86%E8%8A%82)
    - [拓展](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E6%8B%93%E5%B1%95)
  - [红石刻](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E7%BA%A2%E7%9F%B3%E5%88%BB)
  - [电路特征](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E7%94%B5%E8%B7%AF%E7%89%B9%E5%BE%81)
- [基本种类](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%9F%BA%E6%9C%AC%E7%A7%8D%E7%B1%BB)
  - [数字电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E6%95%B0%E5%AD%97%E7%94%B5%E8%B7%AF)
  - [模拟电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E6%A8%A1%E6%8B%9F%E7%94%B5%E8%B7%AF)
  - [机械电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E6%9C%BA%E6%A2%B0%E7%94%B5%E8%B7%AF)
  - [飞行器科技](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E9%A3%9E%E8%A1%8C%E5%99%A8%E7%A7%91%E6%8A%80)
  - [生存实用电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E7%94%9F%E5%AD%98%E5%AE%9E%E7%94%A8%E7%94%B5%E8%B7%AF)
  - [储存电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%82%A8%E5%AD%98%E7%94%B5%E8%B7%AF)
  - [TNT大炮](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#TNT%E5%A4%A7%E7%82%AE)
    - [矢量炮](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E7%9F%A2%E9%87%8F%E7%82%AE)
- [基本电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%9F%BA%E6%9C%AC%E7%94%B5%E8%B7%AF)
  - [脉冲电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E8%84%89%E5%86%B2%E7%94%B5%E8%B7%AF)
  - [时钟电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E6%97%B6%E9%92%9F%E7%94%B5%E8%B7%AF)
  - [传输电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E4%BC%A0%E8%BE%93%E7%94%B5%E8%B7%AF)
    - [纵向传输电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E7%BA%B5%E5%90%91%E4%BC%A0%E8%BE%93%E7%94%B5%E8%B7%AF)
    - [模拟传输](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E6%A8%A1%E6%8B%9F%E4%BC%A0%E8%BE%93)
    - [杂项传输电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E6%9D%82%E9%A1%B9%E4%BC%A0%E8%BE%93%E7%94%B5%E8%B7%AF)
  - [逻辑电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E9%80%BB%E8%BE%91%E7%94%B5%E8%B7%AF)
  - [记忆电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E8%AE%B0%E5%BF%86%E7%94%B5%E8%B7%AF)
  - [杂项电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E6%9D%82%E9%A1%B9%E7%94%B5%E8%B7%AF)
- [建造电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%BB%BA%E9%80%A0%E7%94%B5%E8%B7%AF)
  - [计划](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E8%AE%A1%E5%88%92)
  - [建造](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%BB%BA%E9%80%A0)
  - [解决问题](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E8%A7%A3%E5%86%B3%E9%97%AE%E9%A2%98)
  - [优化](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#-%7Bzh-cn%3A%E4%BC%98%E5%8C%96%3Bzh-tw%3A%E9%9B%BB%E8%B7%AF%E5%84%AA%E5%8C%96%3B%7D-)
- [参考](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%8F%82%E8%80%83)
- [导航](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF#%E5%AF%BC%E8%88%AA)

## 相关资源与材质 (Assets)

红石相关方块/物品贴图通常位于：
- 红石粉：`assets/minecraft/textures/block/redstone_dust_*`
- 中继器/比较器：`assets/minecraft/textures/block/repeater_*`、`comparator_*`
- 红石火把：`assets/minecraft/textures/block/redstone_torch_*`
- 红石灯：`assets/minecraft/textures/block/redstone_lamp_*`
