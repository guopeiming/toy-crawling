# toy-crawling
a toy crawling project

- [ ] 基于`beautifulsoup`的爬虫
- [x] 基于`scrapy`的爬虫
- [x] 基于`flask`的web服务器

#
# 简单说明文档

## 运行方式
1. 运行数据库docker，端口6761
> docker container start pmg-mysql
2. 运行flask  
> cd ./FlaskServer/  
> bash run.sh

## 数据库表结构
1. 爬虫数据表结构  

    id<br>int | source_site<br>varchar(32) | url<br>varchar(128) | article<br>varchar(2048) | create_time<br>datatime  
    ------------ | -------------  | ------- | ------ | ---- |
    1 | www.iie.cas.cn | http://www.iie.cas.cn/xxxx.html | 中国科学院信息工程研究... | 2021-08-05 15:54:28 

2. 爬虫数据表结构  

    id<br>int | create_time<br>datatime | update_time<br>datatime | status<br>varchar(16) | crawler_id<br>varchar(35)  
    ------------ | -------------  | ------- | ------ | ---- |
    1 | 2021-08-11 12:33:46 | 2021-08-11 12:35:01 | finished | 71b8439c41c7323740903528c94a7980 

## 代码说明

爬虫模块主要基于`flask`+`scrapy`+`mysql`实现。  
`flask`提供和业务服务器的web交互，提供两个api。  
`scrapy`负责爬虫，对于新站点的爬取只需添加`xpath`路径即可，相关的站点过滤中间件和数据存储不用管，具有搞拓展性和维护性。
`mysql`提供数据存储。
