# Fabric Modding 开发文档

> 来源: [FabricMC/fabric-docs](https://github.com/FabricMC/fabric-docs) | SHA: b5fc275 | 同步时间: 2026-04-24

## 简介

Fabric 是一个轻量级的 Minecraft: Java Edition 模组工具链，设计简洁易用。它允许开发者对原版游戏进行修改（"mods"），添加新功能或更改现有机制。

本知识库涵盖 Fabric Mod 开发的核心主题，包括：
- 创建 Mod 和环境配置
- 渲染、网络、数据生成等高级主题

---

## 文档分类索引

### 入门指南 (Getting Started)
- [环境配置](Fabric-入门-环境配置.md)
- [创建项目](Fabric-入门-创建项目.md)
- [构建 Mod](Fabric-入门-构建Mod.md)
- [启动游戏](Fabric-入门-启动游戏.md)
- [项目结构](Fabric-入门-项目结构.md)
- [生成源码](Fabric-入门-生成源码.md)
- [打开项目](Fabric-入门-打开项目.md)
- [技巧与窍门](Fabric-入门-技巧与窍门.md)

#### IntelliJ IDEA 配置
- [IntelliJ-IDEA-环境配置](Fabric-入门-IntelliJ-IDEA-环境配置.md)
- [IntelliJ-IDEA-打开项目](Fabric-入门-IntelliJ-IDEA-打开项目.md)
- [IntelliJ-IDEA-生成源码](Fabric-入门-IntelliJ-IDEA-生成源码.md)
- [IntelliJ-IDEA-构建Mod](Fabric-入门-IntelliJ-IDEA-构建Mod.md)
- [IntelliJ-IDEA-启动游戏](Fabric-入门-IntelliJ-IDEA-启动游戏.md)
- [IntelliJ-IDEA-技巧与窍门](Fabric-入门-IntelliJ-IDEA-技巧与窍门.md)

#### VSCode 配置
- [VSCode-环境配置](Fabric-入门-VSCode-环境配置.md)
- [VSCode-打开项目](Fabric-入门-VSCode-打开项目.md)
- [VSCode-生成源码](Fabric-入门-VSCode-生成源码.md)
- [VSCode-启动游戏](Fabric-入门-VSCode-启动游戏.md)
- [VSCode-技巧与窍门](Fabric-入门-VSCode-技巧与窍门.md)

---

### 物品 (Items)
- [第一个物品](Fabric-物品-第一个物品.md)
- [物品模型](Fabric-物品-物品模型.md)
- [物品外观](Fabric-物品-物品外观.md)
- [自定义数据组件](Fabric-物品-自定义数据组件.md)
- [自定义附魔效果](Fabric-物品-自定义附魔效果.md)
- [自定义物品交互](Fabric-物品-自定义物品交互.md)
- [自定义盔甲](Fabric-物品-自定义盔甲.md)
- [自定义工具](Fabric-物品-自定义工具.md)
- [自定义创造模式标签](Fabric-物品-自定义创造模式标签.md)
- [食物](Fabric-物品-食物.md)
- [药水](Fabric-物品-药水.md)
- [刷怪蛋](Fabric-物品-刷怪蛋.md)

---

### 方块 (Blocks)
- [第一个方块](Fabric-方块-第一个方块.md)
- [方块模型](Fabric-方块-方块模型.md)
- [方块状态](Fabric-方块-方块状态.md)
- [方块实体](Fabric-方块-方块实体.md)
- [方块容器](Fabric-方块-方块容器.md)
- [容器菜单](Fabric-方块-容器菜单.md)
- [方块实体渲染器](Fabric-方块-方块实体渲染器.md)
- [方块着色](Fabric-方块-方块着色.md)

---

### 实体 (Entities)
- [第一个实体](Fabric-实体-第一个实体.md)
- [属性](Fabric-实体-属性.md)
- [效果](Fabric-实体-效果.md)
- [伤害类型](Fabric-实体-伤害类型.md)

---

### 命令 (Commands)
- [基础](Fabric-命令-基础.md)
- [参数](Fabric-命令-参数.md)
- [建议](Fabric-命令-建议.md)

---

### 渲染 (Rendering)
- [基础概念](Fabric-渲染-基础概念.md)
- [GUI图形](Fabric-渲染-GUI图形.md)
- [抬头显示](Fabric-渲染-抬头显示.md)
- [世界渲染](Fabric-渲染-世界渲染.md)

#### GUI 组件
- [自定义屏幕](Fabric-渲染-GUI-自定义屏幕.md)
- [自定义组件](Fabric-渲染-GUI-自定义组件.md)

#### 粒子系统
- [创建粒子](Fabric-渲染-粒子-创建粒子.md)

---

### Mixin
- [字节码](Fabric-Mixin-字节码.md)

---

### 数据生成 (Data Generation)
- [设置](Fabric-数据生成-设置.md)
- [配方](Fabric-数据生成-配方.md)
- [战利品表](Fabric-数据生成-战利品表.md)
- [物品模型](Fabric-数据生成-物品模型.md)
- [方块模型](Fabric-数据生成-方块模型.md)
- [进度](Fabric-数据生成-进度.md)
- [标签](Fabric-数据生成-标签.md)
- [翻译](Fabric-数据生成-翻译.md)
- [附魔](Fabric-数据生成-附魔.md)
- [特性](Fabric-数据生成-特性.md)

---

### 流体 (Fluids)
- [第一个流体](Fabric-流体-第一个流体.md)

---

### 声音 (Sounds)
- [使用声音](Fabric-声音-使用声音.md)
- [自定义声音](Fabric-声音-自定义声音.md)
- [动态声音](Fabric-声音-动态声音.md)

---

### Loom (构建工具)
- [索引](Fabric-Loom-索引.md)
- [选项](Fabric-Loom-选项.md)
- [任务](Fabric-Loom-任务.md)
- [类路径组](Fabric-Loom-类路径组.md)
- [Fabric-API](Fabric-Loom-Fabric-API.md)
- [生产运行任务](Fabric-Loom-生产运行任务.md)

---

### 移植 (Porting)
- [索引](Fabric-移植-索引.md)
- [Fabric-API](Fabric-移植-Fabric-API.md)
- [映射](Fabric-移植-映射.md)

---

### 类修改器 (Class Tweakers)
- [索引](Fabric-类修改器-索引.md)
- [接口注入](Fabric-类修改器-接口注入.md)
- [枚举扩展](Fabric-类修改器-枚举扩展.md)
- [访问扩展](Fabric-类修改器-访问扩展.md)

---

### 核心主题
- [总览](Fabric-总览.md)
- [网络](Fabric-网络.md)
- [事件](Fabric-事件.md)
- [编解码器](Fabric-编解码器.md)
- [数据附件](Fabric-数据附件.md)
- [保存数据](Fabric-保存数据.md)
- [调试](Fabric-调试.md)
- [自定义配方类型](Fabric-自定义配方类型.md)
- [文本与翻译](Fabric-文本与翻译.md)
- [自动化测试](Fabric-自动化测试.md)
- [游戏规则](Fabric-游戏规则.md)
- [按键绑定](Fabric-按键绑定.md)

---

## 参考资源

- **Fabric 官网**: https://fabricmc.net/
- **GitHub 仓库**: https://github.com/FabricMC
- **Fabric Wiki**: https://fabricmc.net/wiki/
- **示例 Mod**: https://github.com/FabricMC/fabric-docs/tree/main/reference/latest

## 前提条件

开始 Fabric Mod 开发前，需要具备：
- Java 开发基础
- 面向对象编程（OOP）概念

## Fabric 核心组件

1. **Fabric Loader**: 灵活的 Mod 加载器
2. **Fabric API**: 补充性 API 和工具集
3. **Fabric Loom**: Gradle 插件，简化 Mod 开发和调试
