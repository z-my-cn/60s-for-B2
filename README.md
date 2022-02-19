# 60s早报使用说明

## 配置文件

仅支持Wordpress的B2主题。

配置文件名称为**60s.json**，需要与程序放置在同一目录下。

### api_token

>ALAPI的Token密钥，从[ALAPI用户中心](https://admin.alapi.cn/dashboard/workplace)获取。

### url

>Wordpress的网站地址，带http[s]。

目前仅支持**B2主题**，上传至快讯模块。

### user

>Wordpress的用户信息，用于上传图片和发布内容。

username：用户名；password：密码

### news_tag

>快讯标签，请先在B2主题设置快讯模块添加。

### all_image

是否采用全图模式。

>全图模式：整个页面排版全部为图片，样式美化，但内容文字不可复制。

>非全图模式：除头图外，其余内容均为文本形式，样式单一。

## 运行

### Python 运行

依赖python第三方库**requests**

```shell
cd 60s.py所在目录
python3 60s.py
```

### Linux 运行

>可执行文件下载[release](https://github.com/z-my-cn/60s-for-B2/releases)

```shell
cd 可执行文件60s所在目录
./60s
```
### Windows运行

>可执行文件下载[release](https://github.com/z-my-cn/60s-for-B2/releases)

直接双击60s.exe运行即可

## Q&A

### 如何设置定时执行？

>关于程序定时执行的具体方法请自行百度。

API接口一般在每天1点-2点更新数据，程序带有更新判断，未更新会每隔1800秒请求一次。

### 非全图模式下能不能自定义HTML模板？

由于使用的是B2主题及JWT插件提供的API，快讯提交接口似乎会清楚html代码，没办法改样式。

### 为什么不通过WP自带的接口发布文章？

接上个问题，内容发布在B2主题的快讯模块，而WP-REST-API并没找到对应的发布接口。

>至于Wordpress xmlprc，~~可能存在安全问题。~~

### 将来会不会考虑适配通用WP发布？

或许吧，看时间考虑。

### 代码写的好烂？

>谢谢！我是文科生！这只是一次Python练习。

欢迎大佬斧正！

