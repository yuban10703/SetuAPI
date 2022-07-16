# SetuAPI

**数据库在release里**

API: https://setu.yuban10703.xyz/setu

请求方法:GET,POST

返回数据为JSON

### API文档地址

https://setu.yuban10703.xyz/docs

### 请求字段

| 字段   | 类型      | 说明                                                      |
|------|---------|---------------------------------------------------------|
| r18  | integer | 0:性感,1:色情,2:all                                         |
| num  | integer | 数量,最大50                                                 |
| tags | array[string] | 可以传入多个tag                                               |
| replace_url | HttpUrl | 反代的链接,用于替换默认的https://i.pximg.net  例如https://i.pixiv.cat |

### **返回数据**

| 字段名 | 数据类型 | 说明 |
| ------ | -------- | ---- |
| detail | string  | 没东西就是正常 |
| tags | array[string]  | 你请求的时候发送的tags |
| count | integer  | data内的数据数量 |
| data | array[setu] | setu列表 |

### **setu**

| 字段名 | 数据类型 | 说明 |
| ------ | -------- | ---- |
| artwork |  array[artwork] | 画廊的标题和P站id |
| author | array[author] | 作者的名字和P站ID |
| count | integer  | 获取到的数量 |
| sanity_level | integer | P站给的字段 可能是色情等级吧|
|  r18  |  boolean  |  是否R18 |
| page |  integer  |   作品在画廊的第几P(从0开始算)  |
|  create_date |  string($date-time)  | P站的字段 应该是最后更新日期 |
| size | array[size] | 图片的长宽 |
| tags | array[string]  | 图片的标签 |
| urls | array[urls] | 图片的链接 |

### **artwork**

| 字段名 | 数据类型 | 说明        |
| ------ | -------- | ----------- |
| title  | string   | 作品标题    |
| id     | integer  | 作品的P站ID |

### **author**

| 字段名 | 数据类型 | 说明        |
| ------ | -------- | ----------- |
| name   | string   | 作者名字    |
| id     | integer  | 作者的P站ID |

### **size**

| 字段名 | 数据类型 | 说明 |
| ------ | -------- | ---- |
| width  | integer  | 宽   |
| height | integer  | 高   |

### **urls**

| 字段名   | 数据类型     | 说明     |
| -------- | ------------ | -------- |
| original | string($uri) | 链接(画质:original) |
| large    | string($uri) | 链接(画质:large)   |
| medium   | string($uri) | 链接(画质:medium)  |

### docker

~~~
docker build -t setuapi:v1.7 .
~~~

~~~
docker run -d \
-p 9001:80 \
-e mongodb="mongodb+srv://username:password@cludn.mongodb.net/setu?retryWrites=true&w=majority" \
-e db="setu" \
-e col="setu_v5" \
-e LOG_LEVEL="debug" \
setuapi:v1.7
~~~

### mongodb

要给r18,tags字段分别建索引

### 感谢

https://cloud.mongodb.com

https://vercel.com
