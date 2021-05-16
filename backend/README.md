# Christin

## 注意事项

config/secure.py中存在安全性文件，开放仓库之前需要进行隐藏

改一下mysqloperator的数据库配置

```mysql
# 将安全更新模式解除
SET SQL_SAFE_UPDATES = 0;
```

## 必要说明

用户使用sandbox管理数据库 一个用户默认只有一个sandbox

sandbox 的数据会存储在本地的 `/root/neo4j-data` 中

## 使用说明

必须安装docker、docker-compose

### 环境变量

linux :

```shell
export CHRISTIN_HOST="172.17.0.1"
```

WSL2 && macos:

```shell
export CHRISTIN_HOST="host.docker.internal" 
```

Windows暂无

## 附录

### 关系对照表

['SMIT->SMTT',
'SMHB->SMTS',
'SMHB->SMIT',
'SMTT->SMDE',
'SMTS->SMMS',
'SMMS->SMDE']

Ingredient->Target  
Herb->TCM symptom  
Herb->Ingredient  
Target->Disease TCM  
symptom->MM symptom  
MM symptom->Disease

### Neo Example

MATCH (movie:Movie)<-[review:REVIEWED]-(:User)  
WHERE review.rating < 3 WITH DISTINCT movie MATCH (movie)<-[review:REVIEWED]-(:
User)  
RETURN avg(review.rating) as avgRating ORDER BY avgRating DESC LIMIT 10

MATCH p=()-[r:REL]->()-[]->() RETURN p LIMIT 25


## 常用命令

```shell
pybabel extract -F babel.cfg -o messages.pot .

pybabel update -i messages.pot -d application/translations

pybabel compile -d application/translations

# celery
celery -A application.server.tasks.celery worker --loglevel=INFO --logfile=logs/task.log
```