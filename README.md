# SetuAPI

数据库在release里

### API文档地址

https://setu.yuban10703.xyz/docs


| 字段  | 类型          | 说明                       |
| ----- | ------------- | -------------------------- |
| r18 | integer       | 0:性感,1:色情,2:all |
| num   | integer       | 数量,最大30                |
| tags   | array[string] | 可以传入多个tag            |

**返回值**

| 字段名 | 数据类型 | 说明 |
| ------ | -------- | ---- |
| code | int  | 200为正常,也没有其他返回... |
| tags | array[string]  | 你请求的时候发送的tags |
| count | int  | data内的数据数量 |
| data | array | setu列表 |

### mongodb
要给r18,tags字段分别建索引

### docker
`docker build -t setuapi:v1.7 .
`

`
docker run -d -p 9001:80 -e mongodb="mongodb+srv://username:password@cludn.mongodb.net/setu?retryWrites=true&w=majority" -e db="setu" -e col="setu_v5" -e LOG_LEVEL="debug" setuapi:v1.7
`
### 感谢
https://cloud.mongodb.com
