# Christin
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fzxjlm%2FChristin.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fzxjlm%2FChristin?ref=badge_shield)


## 项目简介

**基于多元异构数据的中医药知识图谱构建及应用** , 主要的工作是从多元异构的数据中提取出知识实体并将其结构化, 然后用这些知识实体去构建知识图谱.

作为其实践产物的平台,我将该平台命名为 _Christin_ , 选名自我所以喜爱的 ARPG 游戏系列 <伊苏> 的主角 _Adol Christin_ 以及我第二喜欢的小说家 _Dame Agatha Mary Clarissa Christie_. 当然, 其正式的平台名称叫做 **中医药知识图谱构建平台**.

其开发的思路和过程记述于 [Christin 开发记录](https://blog.harumonia.moe/christin-develop-1/).

## 平台使用

### 技能要求

如果需要对项目进行再开发, 需要对如下的技能有所了解或掌握. 此外, 最好还要熟悉一种 Linux 操作系统的使用(非图形化).

#### 后端

- Python
  - Flask
  - Celery
  - Spacy

#### 前端

- JavaScript
  - React
  - AntD
  - Graphin
  - neo4j-driver
- HTML
- CSS

#### 中间件

中间件已经配置完毕, 不会并不影响项目的再开发, 不过自定义配置会受到掣肘.

- Nginx
- Docker
- Redis

#### 数据库

- Neo4j
- MySQL

#### 理论

算法理论. 如果需要对模型进行修改, 则需要使用对应的算法理论.

- NLP
  - NER

技术理论方面, 同样是不会不影响开发. 不过这是本平台构建的基石, 推荐重构之前了解以下相关的概念.

- MVP
- Agile Development
  - TDD
  - CI

### 基础依赖

平台的运行存在两个基础的依赖，运行环境中必须具有 **MySQL** 和 **Neo4j** 这两个数据库， 同样，还需要 **Python** .

平台对于环境变量有着基础的配置， 下面内容中涉及到环境变量修改的，可以至 `backend/config/settings.py` 中寻找对应的环境变量名。

#### Python

Python 的版本推荐为 _3.8.5_, 兼容 3.6 及其以上的版本。后续的所有开发将在 3.8.5 的版本下进行开发。

#### MySQL

MySQL 的版本推荐为 _8.0.x_ 。

用户名和密码推荐都为 root， 否则需要在 [环境变量](#环境变量配置) 中进行配置修正。

#### Neo4j

Neo4j 的版本推荐为 _4.2.x_ 或 _3.5.x_, 这两个版本的区别度很大，neo4j 在这两个版本中存在很大的变动， 不够在实际测试中发现，两个版本都能正常运行(截至 2021.04.25)， 后续的图数据库开发将会围绕 _4.x_ 版本进行。

用户名为 _neo4j_ (这是免费版默认的), 密码推荐为 _zxjzxj233_

#### Docker

Docker 的版本推荐为 20.10.6 及以上, 无论使用何种方式运行, Docker 都是必需的.

### 通过 Docker 使用

通过 docker 可以直接运行项目主题程序, 其缺点就是对修改的响应能力很低。使用之前，确保机器能够使用 `docker` 和 `docker-compose`。

- docker version 20.10.6 ^
- docker-compose version 1.29.1 ^

```shell
docker-compose up --build
```

该命令执行之后，静待构建完成，然后访问 _'http://127.0.0.1'_ 即可, **确保你的 80 端口没有被其他进程占用，否则在 docker-compose.yml 文件中修改 nginx 模块的端口**。

### 常规使用

本项目采用完全前后端分离的设计思路， 在常规使用的过程中， 主要考虑如下两个文件夹。

#### backend

backend，即后端. 其详细说明可见于 [backend](https://github.com/zxjlm/Christin/tree/main/backend)

首先参照 [包管理](#包管理) 的内容，安装好之后， 通过如下命令使用。

```shell
flask run
```

> 这一步可能出现的问题：
>
> 1. 数据库连接的问题， 参照 [MySQL](#MySQL)， 考虑可能是环境变量的问题

#### frontend

frontend, 即前端。 其详细说明可见于 [frontend](https://github.com/zxjlm/Christin/tree/main/frontend)

安装好 `yarn` 之后通过如下命令使用。

```shell
yarn install
cross-env REACT_APP_ENV=dev MOCK=none UMI_ENV=dev umi dev
```

完成以上两步之后, 即可访问 localhost:8000 进行项目的使用.

## 注意事项

### 包管理

本项目的包管理使用 [poetry](https://python-poetry.org/) . 版本为 _1.1.4_.

安装完毕之后,在 _backend_ 目录下使用 `poetry install` 命令直接运行， 推荐创建一个新的虚拟环境.

#### 环境管理

> 环境管理工具不影响本项目的使用, 任凭喜好即可。

本项目使用的虚拟环境为 _miniconda_, 推荐 **Mac** 和 **Linux** 系统的同学使用该环境管理.

### 环境变量配置

以下变量在自己机器上运行时 **需要手动配置** .

- CHRISTIN_NEO_HOST : neo4j 地址, 默认为 'localhost'
- CHRISTIN_NEO_PORT : neo4j 端口, 默认为 7687
- CHRISTIN_NEO_PWD : neo4j 密码, 默认为 'zxjzxj233' (用户名默认为 neo4j)

- CHRISTIN_MYSQL_HOST : mysql 地址, 默认为 'localhost'
- CHRISTIN_MYSQL_PORT : mysql 使用的端口, 默认为 3306
- CHRISTIN_MYSQL_USER : mysql 登录用户名, 默认为 root
- CHRISTIN_MYSQL_PWD : mysql 登录用户密码, 默认为 root

以下变量在一般情况下按照默认配置即可.

- APP_SETTINGS : APP 运行模式

- CHRISTIN_REDIS_HOST : redis 地址

- CELERY_BROKER_URL : celery 链路配置
- CELERY_RESULT_BACKEND : celery 结果链路配置

- API_URL : api 的开放地址
- CHRISTIN_MAIL_USER : 邮箱账户 ( 邮箱可能存在过期的情况, 建议 2021.9 之后使用进行手动配置 )
- CHRISTIN_MAIL_PWD : 邮箱密码

## 后续联系方式

推荐以邮件进行联系.

QQ: 1391440047 (需要注明身份信息)
Mail: zxjlm233@gmail.com (标注为 _毕设问题_)


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fzxjlm%2FChristin.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fzxjlm%2FChristin?ref=badge_large)