# frontend

## 概述

前端使用 React 技术,采用 AntD Pro 框架开发, 共计存在 3 个主要页面. 根据前后端分离的设计理念, 前端完全依靠 api 进行交互, 过程中不存在 SSR 的环节.

### 登录页面

登录页面在原始的 AntD 的页面上进行修改, 其界面如下图所示.

![截屏2021-06-05 上午9.05.08.png](https://i.loli.net/2021/06/05/xp8MD62KPcRQSTI.png)

### 主页面

主页面采用经典的 AntD Pro 布局, 共分为四个子模块.

- 欢迎
- 项目创建
- 项目管理
- 基础数据管理

![截屏2021-06-05 上午9.06.06.png](https://i.loli.net/2021/06/05/Seq7YpgLORPx1uD.png)

### 图数据库可视化页面

![截屏2021-06-05 上午9.12.59.png](https://i.loli.net/2021/06/05/85pS3TM1hP6BvE2.png)

## 使用

前端本身并没有 mock 数据, 需要开启后端程序搭配使用.

```shell
# 安装依赖
yarn install

# 运行项目
cross-env REACT_APP_ENV=dev MOCK=none UMI_ENV=dev umi dev

# 构建项目
yarn build
```
