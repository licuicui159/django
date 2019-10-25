# 面试必杀技

## QuerySet.query

print(QuerySet.query) 可查看当前orm语句具体执行的SQL语句

## 查看日志

1.开启日志监控

mysql> show variables like 'general%';

mysql> set global general_log = 'ON';

mysql> show variables like 'general%';   #确定状态为ON时，general_log_file 值对应的 文件地址中 /var/lib/mysql/tarena.log 可查看 所有发到mysql的语句

2.如果是ON，新终端查看日志

tarena@tarena:~$ sudo su

root# tail -f /var/lib/mysql/tarena.log 

3.进入shell可进行orm语句测试

注意：objects.xxx命令为惰性取值，只有在调用的时候，才发出sql语句

​	s = book.objects.all()

​	s[0]切片/索引时，会调用sql语句

​	迭代s的时候，会调用sql语句

​	print(s)会调用sql语句

特别注意，每次执行QuerySet[0]则都进行sql语句调用，所以每次执行均是一个新对象

建议使用具体对象进行 更新时，执行右侧->obj = QuerySet[0]

4.必须关闭，否则容易撑爆磁盘

mysql> set global general_log = 'OFF';

mysql> show variables like 'general%'; 





## 哈希三大特点

定长输出【无论输入多长，输出都是定长】、雪崩【一变则巨变】、不可逆【无法反算回明文】

自行处理密码存储策略
1.当用户注册时，将用户传递过来的明文密码进行 如 md5,sha系列的哈希算法【散列】；
 pw=request.POST.get('password')
 pw += 'salt'
 import hashlib
 m5 = hashlib.md5()
 m5.update(pw.encode())
 pw_md5 = md5.hexdigest()

2.当用户登录时

用户登录时填写的密码

pw = request.POST.get('password')
pw += 'salt'
import hashlib
m5 = hashlib.md5()
m5.update(pw.encode())
pw_md5 = md5.hexdigest()

user = User.objects.get(username=username)
if user.password != pw_md5：
	return '用户名或密码错误'

## 缓存总结

​	1.后端缓存

​		我们将复制视图函数处理结果放到其他存储介质中，当用户下次访问该视图函数时，可跳过视图函数直接将结果从存储介质中获取并返回给用户。

 2. 浏览器缓存

    每次浏览器发出请求时【浏览器地址栏回车/摁钮/超链接-get】,浏览器优先检查是自己浏览器内部的缓存区域是否有数据，

    ​	1.如果没有强缓存，浏览器发出HTTP请求至服务器端

    ​	2.协商缓存 - 【Last_Modified/Etag】，原来有强缓存-但是此次请求检查时，缓存过期：

​				尝试协商缓存的结果：

​					1.Last_Modifide

​							把上次缓存响应头中的Last_Modifide的值赋值给if-Modifide-Since请求头，发送至服务器，如果服务器端对比当前响应的Modifide和请求头中一致，则返回304且响应体为空；否则返回200，响应全新数据

```
304：代表当前缓存能用，您再使用一阵子，响应体为空

200：缓存的确过期了，响应中携带最新数据
```

​					2.Etag  

​							把上次缓存响应头中的Etag的值赋值给if-None-Match请求头，剩余步骤同上

3.csrf 跨站伪造攻击

​	1.攻击原理：老王看直播【每天，高频次】

​	2.Django如何防范：

​		1.一定要确定是否开启csrf中间件

​		2.模板表单中添加新标签

```
form标签内{% csrf_token %}
```

​		3.cookies里面 暗号1，表单里面 暗号2 ，服务器端效验暗号1 == 暗号2 ！如果成立，则效验通过，否则 怀疑是 csrf 攻击

## 获取客户端ip,路由

- request.META['REMOTE_ADDR'] 可以得到远程客户端的IP地址
- request.path_info 可以得到客户端访问的GET请求路由信息

## CentOS 7x

#  Django Web框架笔记

### 目录
[TOC]

- 课程特点：
    1. 学习难度大，大部分内容需要理解并记忆
    2. 文件较多易混淆
    3. 学习阶段注重框架使用，工作阶段注重实现业务逻辑
    4. 综合应用强，小练习少

### 要点1

Django  -  框架 -  web工具箱  -  web基础配置 + 路由分发 + 视图函数

django-admin startproject  项目名 

1） manage.py       ->   python3 manage.py  runserver  -> 开启调试环境[127.0.0.1:8000]

2） 项目名 - 文件夹 ->  settings.py  urls.py    wsgi.py



URL   http://127.0.0.1:8000/abc/ddd?username=xiaonao&age=18#topic

urls.py ->

```python
   urlpatterns = [
		url(r'xxxxx',  views.xxx),
        ...
        ...
]
    
  1.分组
	r'^page(\d+)'  ->  page_view(request, n)  [django采用位置传参调用对应的视图函数]
  2.命名分组
	r'^page(?P<name>\d+)' -> page_view(request, name) [django采用关键字传参调用对应的视图函数]
    
    
```

视图函数 ->   项目同名目录下 创建了 views.py  ->  

def  xxx_view(request,  xx):

	return  HttpResponse/HttpResponseRedirect



请求和响应

GET、POST

request.属性名

if  request.method == 'GET'/'POST':

      request.GET.get('a', 默认值) 
    
      request.GET.getlist('a')   -> 相同变量名  多个不同的值

请求头 - Content-Type  - 提交数据的格式

	GET -  由于请求体 为空，所以请求头中没有 该头
	
	POST - 一定会有该头
	
		1，html中  如果使用form标签 进行post提交，则浏览器会将该头的值赋值为  application/x-www-form-urlencoded [ Django中 检查到此次请求是该头的时候，可以使用 request.POST 取值]
	
		2，非表单提交  Django中 使用 reuqest.body 取 请求体的值

响应：

	视图函数 返回一个 响应对象  HttpRespons[xxx]
	
	code  200/302/404/403/500 
	
	响应头 
	
	Content-Type  -  text/html; charset=utf-8 
	
	Location   -  302返回时携带此头， 标记跳转的目的地	
### 要点2

1 设计模式 MVC  + MTV

	MVC  -   C 控制层 - 大脑  ；  M模型层 - 数据库交互 ；  V视图层 - 用户层面显示效果
	
	MTV  -  c-urls.py -主路由 ；  M模型层 ；  V视图层 - 业务逻辑;   T模板层-负责html显示

2  模板

	1，配置settings.py   TEMPLATES
	
		DIRS = [os.path.join(BASE_DIR, 'templates'), ]          #当前项目 html存储位置
	
	2,  view层调用
	
		1， t = loader.get_template('模板文件名')
	
			html = t.render('字典')
	
			return HttpResponse(html)
	
		2,   from django.shortcuts import render
	
			dic = {'username': 'guoxiaonao'}
	
			return render(request,  'xxx.html',  dic)
	
			return render(request, 'xxx.html', locals())
	
	3,  调用    {{ 变量名 }}  {{ username }}
	
	4,  {%  标签  %}   -  流程控制    if   for
	
		{% if %}业务逻辑{% endif %}
	
	5,  过滤器   {{  变量|过滤器: 参数名  }}
	
	6,  模板继承   
	
			父模板    {% block 块名 %}xxxx{% endblock %}  
	
			子模板
	
				{% extends  'base.html' %}
	
				{% block  '父模板的块名' %}
	
					xxxxxx
	
				{% endblock %}

###要点 - 增删改查

1，创建数据

	1，MyModel.objects.create(属性=值)
	
	2，obj = MyModel(属性=值)  ->  obj.属性 = 值  -> obj.save()

2，查询

	1，MyModel.objects.all()  -> 全量查询 [obj1, obj2]
	
	2，MyModel.objects.values('列1'，'列2') -> 按列查询 [{},{}]
	
	3，MyModel.objects.values_list('列1'，'列2')  -> [(),()]
	
	4，order_by('列1'， '-列2')  ->  '-' ： 倒序
	
	5，filter(条件)
	
		1，等值查询  (属性=值,  属性2=值 , .....)    and 等值查询
	
		2，查询谓词  （price_gte = 50）
	
	6，exclude(条件)    ->  筛选出条件之外的数据集合
	
	7，get(条件)  ->  取多了报错，没取到也报错  -> try - except

修改数据  

	1，单个数据
	
		1，查   【get/filter()[索引]】
	
		2，改     obj.属性 = 值
	
		3，存     obj.save() 
	
	2，多个数据【QuerySet】
	
		QuerySet.update(属性=值)

删除

	1，单个数据
	
		1，查
	
		2，删	obj.delete()
	
	2，多个数据
	
		QuerySet.delete()



	3， 伪删除  -  isActive - True活跃的  /  False 非活跃的【即删除】   
	
		ex:  Book中表中添加  isActive 字段【布尔型】 - 默认值 True


## Django框架的介绍

- 2005年发布,采用Python语言编写的开源web框架
- 早期的时候Django主做新闻和内容管理的
- 一个重量级的 Python Web框架，Django 配备了常用的大部分组件
    1. 基本配置
    1. 路由系统
    1. 原生HTML模板系统
    1. 视图 view
    1. Model模型,数据库连接和ORM数据库管理
    1. 中间件
    1. Cookie & Seesion
    1. 分页
    1. 数据库后台管理系统admin

- Django的用途
    - 网站后端开发
    - 微信公众号、微信小程序等后台开发
    - 基于HTTP/HTTPS协议的后台服务器开发
        - 在线语音/图像识别服务器
        - 在线第三方身份验证服务器等
- Django的版本
    - 最新版本:2.2.x
    - 当前教学版本:1.11.8

- Django的官网
    - 官方网址: <http://www.djangoproject.com>
    - 中文文档(第三方):
        - <https://yiyibooks.cn/>
        - <http://djangobook.py3k.cn/>
    - Django的离线文档
        1. 解压缩数据包 `django-docs-1.11-en.zip`
        2. 用浏览器打开 `django-docs-1.11-en/index.html`


### Django的安装
- 查看已安装的版本
    ```python
    >>> import django
    >>> print(django.VERSION)
    (1, 11, 8, 'final', 0)
    ```
- 安装
    1. 在线安装
        - `$ sudo pip3 install django`  安装django的最新版本
        - 或
        - `$ sudo pip3 install django[==版本]` 安装django的指定版本
        - 如:
            - `$ sudo pip3 install django==1.11.8`
    2. 离线安装
        - 下载安装包:
        - 安装离线包
            - `$ tar -xvf Django-1.11.8.tar.gz`
            - `$ cd Django-1.11.8`
            - `$ sudo python3 setup.py install`
    3. 用wheel离线安装
        - 下载安装包:
            - `pip3 download -d /home/tarena/django_packs django==1.11.8`
        - 安装离线包
          - $ pip3 install Django-1.11.8.whl
- Django的卸载
  
- $ pip3 uninstall django
  
- Django 的开发环境
    - Django 1.11.x 支持 Python 2.7, 3.4, 3.5 和 3.6（长期支持版本 LTS)
    - 注: Django 1.11.x 不支持 Python 3.7

### django安装提示

```shell
1,安装celery sudo pip3 install celery
2,安装成功后检查 版本
	1，Django    pip3 freeze|grep 'Django'   1.11.8
    2，celery    pip3 freeze|grep 'celery'   4.3.0

	如果版本不对，请执行 卸载 + 指定版本安装  ex:
	卸载 ->  sudo pip3 uninstall Django
	指定版本安装 ->  sudo pip3 install Django==1.11.8

ps: 安装中途 出现红字报错， 请先翻译一下，大概率是 限+网络不太好

```

## Django框架开发
### 创建项目的指令
  - $ django-admin startproject 项目名称
  - 如:
    
    - $ django-admin startproject mysite1
  - 运行
    ```shell
    $ cd mysite1
    $ python3 manage.py runserver
    # 或
    $ python3 manage.py runserver 5000  # 指定只能本机使用127.0.0.1的5000端口访问本机
    ```
### Django项目的目录结构
- 示例:
    ```shell
    $ django-admin startproject mysite1
    $ tree mysite1/
    mysite1/
    ├── manage.py
    └── mysite1
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py

    1 directory, 5 files
    ```
    
- 项目目录结构解析:
    - manage.py
        - 此文件是项目管理的主程序,在开发阶段用于管理整个项目的开发运行的调式
        - `manage.py` 包含项目管理的子命令, 如:
            - `python3 manage.py runserver` 启动服务
            - `python3 manage.py startapp` 创建应用
            - `python3 manage.py migrate` 数据库迁移
            - `...`
    - mysite1 项目包文件夹
        - 项目包的主文件夹(默认与项目名称一致)
        1. `__init__.py`
            - 包初始化文件,当此项目包被导入(import)时此文件会自动运行
        2. `wsgi.py`
            - WSGI 即 Web Server Gateway Interface
            - WEB服务网关接口的配置文件，仅部署项目时使用
        3. `urls.py`
            - 项目的基础路由配置文件，所有的动态路径必须先走该文件进行匹配
        4. `settings.py`
            - Django项目的配置文件, 此配置文件中的一些全局变量将为Django框架的运行传递一些参数
            - setting.py 配置文件,启动服务时自动调用，
            - 此配置文件中也可以定义一些自定义的变量用于作用全局作用域的数据传递

- `settings.py` 文件介绍
  
    https://docs.djangoproject.com/en/1.11/ref/settings/
    
    1. `BASE_DIR`
       
        - 用于绑定当前项目的绝对路径(动态计算出来的), 所有文件都可以依懒此路径
    2. `DEBUG`
       
        - 用于配置Django项目的启用模式, 取值:
            1. True 表示开发环境中使用 `调试模式`(用于开发中)
            2. False 表示当前项目运行在`生产环境中`(不启用调试)
    3. `ALLOWED_HOSTS`
       
        - 设置允许访问到本项目的网络地址列表,取值:
            1. [] 空列表,表示只有`127.0.0.1`, `localhost`能访问本项目
            2. ['*']，表示任何网络地址都能访问到当前项目
            3. ['192.168.1.3', '192.168.3.3'] 表示只有当前两个主机能访问当前项目
            - 注意:
                - 如果要在局域网其它主机也能访问此主机,启动方式应使用如下模式:
        - `python3 manage.py runserver 0.0.0.0:5000` # 指定网络设备所有主机都可以通过5000端口访问(需加`ALLOWED_HOSTS = ['*']`) 
        
    4. `INSTALLED_APPS`
       
        - 指定当前项目中安装的应用列表
    5. `MIDDLEWARE`
       
        - 用于注册中间件
    6. `TEMPLATES`
       
        - 用于指定模板的配置信息
    7. `DATABASES`
       
        - 用于指定数据库的配置信息
    8. `LANGUAGE_CODE`
       
        - 用于指定语言配置
        - 取值:
            - 英文 : `"en-us"`
            - 中文 : `"zh-Hans"`
    9. `TIME_ZONE`
       
        - 用于指定当前服务器端时区
        - 取值:
            - 世界标准时间: `"UTC"`
            - 中国时区 : `"Asia/Shanghai"`
    10. `ROOT_URLCONF`
        
        - 用于配置根级 url 配置 'mysite1.urls'
        - 如:
            - `ROOT_URLCONF = 'mysite1.urls'`
    
    > 注: 此模块可以通过 `from django.conf import settings` 导入和使用


### URL 介绍
- url 即统一资源定位符 Uniform Resource Locator
- 作用:
  
    - 用来表示互联网上某个资源的地址。
- 说明:
  
    - 互联网上的每个文件都有一个唯一的URL，它包含的信息指出文件的位置以及浏览器应该怎么处理它。
- URL的一般语法格式为：
    ```
    protocol :// hostname[:port] / path [?query][#fragment]
    ```
- 如:
    ```
    http://tts.tmooc.cn/video/showVideo?menuId=657421&version=AID201908#subject
    ```

- 说明:
    - protocol（协议）
        - http 通过 HTTP 访问该资源。 格式 `HTTP://`
        - https 通过安全的 HTTPS 访问该资源。 格式 `HTTPS://`
        - file 资源是本地计算机上的文件。格式: `file:///`
        - ...

    - hostname（主机名）
        - 是指存放资源的服务器的域名系统(DNS) 主机名、域名 或 IP 地址。
        
    - port（端口号）
        - 整数，可选，省略时使用方案的默认端口；
        - 各种传输协议都有默认的端口号，如http的默认端口为80。https默认 443
    - path（路由地址）
        - 由零或多个“/”符号隔开的字符串，一般用来表示主机上的一个目录或文件地址。路由地址决定了服务器端如何处理这个请求

    - query(查询)
        - 可选，用于给动态网页传递参数，可有多个参数，用“&”符号隔开，每个参数的名和值用“=”符号隔开。
    - fragment（信息片断）
        - 字符串，用于指定网络资源中的片断。例如一个网页中有多个名词解释，可使用fragment直接定位到某一名词解释。
    - 注: [] 代表其中的内容可省略


### 视图函数(view)
- 视图函数是用于接收一个浏览器请求并通过HttpResponse对象返回数据的函数。此函数可以接收浏览器请求并根据业务逻辑返回相应的内容给浏览器
- 视图处理的函数的语法格式:
    ```python
    def xxx_view(request[, 其它参数...]):
        
        return HttpResponse对象
    ```
- 参数:
  
    - request用于绑定HttpRequest对象，通过此对象可以获取浏览器的参数和数据
- 示例:
    - 视图处理函数 `views.py` 
        ```python
        # file : <项目名>/views.py
        from django.http import HttpResponse
        def page1_view(request):
            html = "<h1>这是第1个页面</h1>"
            return HttpResponse(html)
        ```

### Django 中的路由配置
- settings.py 中的`ROOT_URLCONF` 指定了主路由配置列表urlpatterns的文件位置
- urls.py 主路由配置文件
    ```python
    # file : <项目名>/urls.py
    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        ...  # 此处配置主路由
    ]
    ```
    > urlpatterns 是一个路由-视图函数映射关的列表,此列表的映射关系由url函数来确定

3. url() 函数
    - 用于描述路由与视图函数的对应关系
    - 模块
        - `from django.conf.urls import url`
    - 语法:
        - url(regex, views, name=None)
        - 参数：
            1. regex: 字符串类型，匹配的请求路径，允许是正则表达式
            2. views: 指定路径所对应的视图处理函数的名称
            3. name: 为地址起别名，在模板中地址反向解析时使用
    
    > 每个正则表达式前面的r表示`'\'`不转义的原始字符串



- 练习
    - 建立一个小网站:
        - 输入网址: http://127.0.0.1:8000, 在网页中输出 : 这是我的首页
        - 输入网址: http://127.0.0.1:8000/page1, 在网页中输出 : 这是编号为1的网页
        - 输入网址: http://127.0.0.1:8000/page2, 在网页中输出 : 这是编号为2的网页
        > 提示: 主页路由的正则是  `r'^$'`
        - 思考
            - 建立如上一百个网页该怎么办？

#### 带有分组的路由和视图函数
- 在视图函数内，可以用正则表达式分组 `()` 提取参数后用函数位置传参传递给视图函数
- 一个分组表示一个参数,多个参数需要使用多个分组,并且使用个/隔开
    - 如:
        - http://127.0.0.1:8000/year/2018/09/27
        - http://127.0.0.1:8000/year/2019
        - http://127.0.0.1:8000/year/????  # 四位数字
- 练习：
    - 定义一个路由的格式为:
        - http://127.0.0.1:8000/整数/操作字符串/整数

    - 从路由中提取数据，做相应的操作后返回给浏览器
    - 如：
    ```
    输入: 127.0.0.1:8000/100/add/200
        页面显示结果：300
    输入: 127.0.0.1:8000/100/sub/200
        页面显示结果：-100
    输入: 127.0.0.1:8000/100/mul/200
        页面显示结果：20000
    ```

#### 带有命名分组的路由和视图函数
- 在url 的正则表达式中可以使用命名分组(捕获分组)
- 说明:
  
    - 在视图函数内，可以用正则表达式分组 `(?P<name>pattern)` 提取参数后用函数关键字传参传递给视图函数
- 示例:
    - 路由配置文件
        ```python
        # file : <项目名>/urls.py
        # 以下示例匹配
        # http://127.0.0.1:8000/person/xiaoming/20
        # http://127.0.0.1:8000/person/xiaohong/29
        # http://127.0.0.1:8000/person/xiaolan/9
        urlpatterns = [
            url(r'^admin/', admin.site.urls),
            url(r'^person/(?P<name>\w+)/(?P<age>\d{1,2})',views.person_view),
        ]
        ```
- 练习:
    - 访问地址:
        - http://127.0.0.1:8000/birthday/四位数字/一到两位数字/一到两位数字
        - http://127.0.0.1:8000/birthday/一到两位数字/一到两位数字/四位数字
    - 最终输出: 生日为: xxxx年xx月xx日
    - 如:
        输入网址: http://127.0.0.1:8000/birthday/2015/12/11
        显示为: 生日为:2015年12月11日
        输入网址: http://127.0.0.1:8000/birthday/2/28/2008
        显示为: 生日为:2008年2月28日
    - 


## HTTP协议的请求和响应
- 请求是指浏览器端通过HTTP协议发送给服务器端的数据
- 响应是指服务器端接收到请求后做相应的处理后再回复给浏览器端的数据

![请求和向应](images/request_response.png)


### HTTP 请求
- 根据HTTP标准，HTTP请求可以使用多种请求方法。
- HTTP1.0定义了三种请求方法： GET, POST 和 HEAD方法(最常用)
- HTTP1.1新增了五种请求方法：OPTIONS, PUT, DELETE, TRACE 和 CONNECT 方法。
- HTTP1.1 请求详述
    | 序号 |  方法   | 描述                                                         |
    | :--: | :-----: | :----------------------------------------------------------- |
    |  1   |   GET   | 请求指定的页面信息，并返回实体主体。                         |
    |  2   |  HEAD   | 类似于get请求，只不过返回的响应中没有具体的内容，用于获取报头 |
    |  3   |  POST   | 向指定资源提交数据进行处理请求（例如提交表单或者上传文件）。数据被包含在请求体中。POST请求可能会导致新的资源的建立和/或已有资源的修改。 |
    |  4   |   PUT   | 从客户端向服务器传送的数据取代指定的文档的内容。             |
    |  5   | DELETE  | 请求服务器删除指定的页面。                                   |
    |  6   | CONNECT | HTTP/1.1协议中预留给能够将连接改为管道方式的代理服务器。     |
    |  7   | OPTIONS | 允许客户端查看服务器的性能。                                 |
    |  8   |  TRACE  | 回显服务器收到的请求，主要用于测试或诊断。                   |


- HttpRequest对象
    - 视图函数的第一个参数是HttpRequest对象
    - 服务器接收到http协议的请求后，会根据请求数据报文创建HttpRequest对象
    - HttpRequest属性
        - path：字符串，表示请求的路由信息
        - path_info: URL字符串
        - method：字符串，表示HTTP请求方法，常用值：'GET'、'POST'
        - encoding：字符串，表示提交的数据的编码方式
            - 如果为None则表示使用浏览器的默认设置，一般为'utf-8'
            - 这个属性是可写的，可以通过修改它来修改访问表单数据使用的编码，接下来对属性的任何访问将使用新的encoding值
        - GET：QueryDict查询字典的对象，包含get请求方式的所有数据
        - POST：QueryDict查询字典的对象，包含post请求方式的所有数据
        - FILES：类似于字典的对象，包含所有的上传文件信息
        - COOKIES：Python字典，包含所有的cookie，键和值都为字符串
        - session：似于字典的对象，表示当前的会话，
        - body: 字符串，请求体的内容(POST或PUT)
        - environ: 字符串,客户端运行的环境变量信息
        - scheme : 请求协议('http'/'https')
        - request.get_full_path() : 请求的完整路径
        - request.get_host() : 请求的主机
        - request.META : 请求中的元数据(消息头)
            - request.META['REMOTE_ADDR']  : 客户端IP地址

### HTTP 响应
- 当浏览者访问一个网页时，浏览者的浏览器会向网页所在服务器发出请求。当浏览器接收并显示网页前，此网页所在的服务器会返回一个包含HTTP状态码的信息头用以响应浏览器的请求。
- HTTP状态码的英文为HTTP Status Code。
- 下面是常见的HTTP状态码：
    - 200 - 请求成功
    - 301 - 资源（网页等）被永久转移到其它URL
    - 404 - 请求的资源（网页等）不存在
    - 500 - 内部服务器错误

- HTTP状态码分类
    - HTTP状态码由三个十进制数字组成，第一个十进制数字定义了状态码的类型，后两个数字没有分类的作用。HTTP状态码共分为5种类型：

        | 分类 | 分类描述                                       |
        | :--: | ---------------------------------------------- |
        | 1**  | 信息，服务器收到请求，需要请求者继续执行操作   |
        | 2**  | 成功，操作被成功接收并处理                     |
        | 3**  | 重定向，需要进一步的操作以完成请求             |
        | 4**  | 客户端错误，请求包含语法错误或无法完成请求     |
        | 5**  | 服务器错误，服务器在处理请求的过程中发生了错误 |

- Django中的响应对象HttpResponse:
    - 构造函数格式:
      
        - `HttpResponse(content=响应体, content_type=响应体数据类型, status=状态码)`
    - 作用:
      
        - 向客户端浏览器返回响应，同时携带响应体内容
    - 参数:
        - content：表示返回的内容。
        - status_code：返回的HTTP响应状态码(默认为200)。
        - content_type：指定返回数据的的MIME类型(默认为"text/html")。浏览器会根据这个属性，来显示数据。如果是text/html，那么就会解析这个字符串，如果text/plain，那么就会显示一个纯文本。
            - 常用的Content-Type如下：
                - `'text/html'`（默认的，html文件）
                - `'text/plain'`（纯文本）
                - `'text/css'`（css文件）
                - `'text/javascript'`（js文件）
                - `'multipart/form-data'`（文件提交）
                - `'application/json'`（json传输）
            - `'application/xml'`（xml文件）
            
            > 注： 关键字MIME(Multipurpose Internet Mail Extensions)是指多用途互联网邮件扩展类型。
    
- HttpResponse 子类
    | 类型                    | 作用           | 状态码 |
    | ----------------------- | -------------- | ------ |
    | HttpResponseRedirect    | 重定响         | 302    |
    | HttpResponseNotModified | 未修改         | 304    |
    | HttpResponseBadRequest  | 错误请求       | 400    |
    | HttpResponseNotFound    | 没有对应的资源 | 404    |
    | HttpResponseForbidden   | 请求被禁止     | 403    |
    | HttpResponseServerError | 服务器错误     | 500    |



### GET方式传参
- GET请求方式中可以通过查询字符串(Query String)将数据传递给服务器    
- URL 格式: `xxx?参数名1=值1&参数名2=值2...`
  
    - 如: `http://127.0.0.1:8000/page1?a=100&b=200`
- 服务器端接收参数
    1. 判断 request.method 的值判断请求方式是否是get请求
        ```python
        if request.method == 'GET':
            处理GET请求时的业务逻辑
        else:
            处理其它请求的业务逻辑
        ```
    2. 获取客户端请求GET请求提交的数据
        1. 语法
            ```python
            request.GET['参数名']  # QueryDict
            request.GET.get('参数名','默认值')
            request.GET.getlist('参数名')
            # mypage?a=100&b=200&c=300&b=400
            
            
            # request.GET=QueryDict({'a':['100'], 'b':['200','400'], 'c':['300']})
            # a = request.GET['a']
            # b = request.GET['b']  # Error
            
            
            ```
        2. 能够产生get请求方式的场合
            1. 地址栏手动输入, 如: http://127.0.0.1:8000/mypage?a=100&b=200
            2. `<a href="地址?参数=值&参数=值">`
            3. form表单中的method为get
                ```html
                #当前form 提交请求至 http://127.0.0.1:8000/user/login
                
                <form method='get' action="/user/login">
                    姓名:<input type="text" name="uname">
                </form>  
                ```
> 一般查询字符串的大小会受到浏览器的的限制(不建议超过2048字节)

- 练习:
    - 访问地址:<http://127.0.0.1:8000/sum?start=整数&stop=整数&step整=字>
    - 输出结果为sum(range(start, step, stop)) 和:
    - 如:
        - 输入网址: http://127.0.0.1:8000/sum?start=1&stop=101&step=1
        - 页面显示: 结果: 5050
        - 输入网址: http://127.0.0.1:8000/sum?stop=101&step=2
        - 页面显示: 结果: 2550
        - 输入网址: http://127.0.0.1:8000/sum?start=1&stop=101&step=2
        - 页面显示: 结果: 2500

- 练习:
    - 访问地址:<http://127.0.0.1:8000/birthday?year=四位整数&month=整数&day=整数>
    - 最终输出: 生日为: xxxx年xx月xx日
    - 如:
        - 输入网址: http://127.0.0.1:8000/birthday?year=2015&month=12&day=11
        - 显示为: 生日为:2015年12月11日



### POST传递参数

- 客户端通过表单等POST请求将数据传递给服务器端,如:

```html
<form method='post' action="/login">
    姓名:<input type="text" name="username">
    <input type='submit' value='登陆'>
</form>
```

- 服务器端接收参数

  - 通过 request.method 来判断是否为POST请求,如:

  ```python
  if request.method == 'POST':
      处理POST请求的数据并响应
  else:
      处理非POST 请求的响应
  ```

- 使用post方式接收客户端数据

  1. 方法

  ```python
  request.POST['参数名']  # request.POST 绑定QueryDict
  request.POST.get('参数名','')
  request.POST.getlist('参数名')
  ```

- 取消csrf验证,否则Django将会拒绝客户端发来的POST请求

  - 取消 csrf 验证

    - 删除 settings.py 中 MIDDLEWARE 中的 CsrfViewsMiddleWare 的中间件

    ```python
    MIDDLEWARE = [
        ...
        # 'django.middleware.csrf.CsrfViewMiddleware',
        ...
    ]
    ```

### form 表单的name属性

- 在form表单控件提交数据时，会自动搜索本表单控件内部的子标签的name属性及相应的值，再将这些名字和值以键-值对的形式提交给action指定的服务器相关位置

- key1=value1&key2=value2&key3=value3

- 在form内能自动搜集到的name属性的标签的控件有

  ```html
  <input name='xxx'>
  <select name='yyy'></select>
  <textarea name='zzz'></textarea>
  ```

  - 如:

  ```html
  <form action="/page1" method="POST">
      <input name="title" type="text" value="请输入">
      <select name="gender">
          <option value=1>男</option>
          <option value=0>女</option>
      </select>
      <textarea name="comment" rows="5" cols="10">附言...</textarea>
      <input type="submit" value="提交">
  </form>
  ```

    

## 注意事项：

```python
1，若启动django时【python3 manage.py runserver】报如下错误：
Error: That port is already in use.
    解决方案：
    	分析：当前有其他进程占用8000端口，
        方案1：ps aux|grep 'manage'  ->  sudo kill -9 进程id
        方案2：更换端口启动   python3 manage.py runserver 8080
    
```

## Django的框架设计模式

- MVC 设计模式
    - MVC 代表 Model-View-Controller（模型-视图-控制器） 模式。
    - 作用: 降低模块间的耦合度(解耦)
    - MVC
        - M 模型层(Model), 主要用于对数据库层的封装
        - V 视图层(View), 用于向用户展示结果
        - C 控制(Controller ，用于处理请求、获取数据、返回结果(重要)
    - MVC模式如图:
        ![](images/mvc.png)
- MTV 模式
    MTV 代表 Model-Template-View（模型-模板-视图） 模式。这种模式用于应用程序的分层开发
    - 作用: 
        - 降低模块间的耦合度(解耦)
    - MTV 
        - M -- 模型层(Model)  负责与数据库交互
        - T -- 模板层(Template)  负责呈现内容到浏览器
        - V -- 视图层(View)  是核心，负责接收请求、获取数据、返回结果
    - MTV模式如图:
        ![](images/mtv.png)

## 模板 Templates
- 什么是模板
    1. 模板是可以根据字典数据动态变化的html网页
    2. 模板可以根据视图中传递的字典数据动态生成相应的HTML网页。

- 模板的配置
    - 创建模板文件夹`<项目名>/templates`
    - 在 settings.py 中有一个 TEMPLATES 变量
        1. BACKEND : 指定模板的引擎
        2. DIRS : 模板的搜索目录(可以是一个或多个)
        3. APP_DIRS : 是否要在应用中的 `templates` 文件夹中搜索模板文件
        4. OPTIONS : 有关模板的选项

- 默认的模块文件夹`templates`
- 修改settings.py文件，设置TEMPLATES的DIRS值为`'DIRS': [os.path.join(BASE_DIR, 'templates')],`
```python
# file: settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 添加模板路径
        'APP_DIRS': True,  # 是否索引各app里的templates目录
        ...
    },
]
```

3. 模板的加载方式
    1. 通过 loader 获取模板,通过HttpResponse进行响应
        ```python
        from django.template import loader
        # 1.通过loader加载模板
        t = loader.get_template("模板文件名")
        # 2.将t转换成 HTML 字符串
        html = t.render(字典数据)
        # 3.用响应对象将转换的字符串内容返回给浏览器
        return HttpResponse(html)
        ```
    2. 使用 render() 直接加载并响应模板
        ```python
        from django.shortcuts import render
        return render(request,'模板文件名', 字典数据)
        ```

###  Django 模板语言

#### 模板的传参
- 模板传参是指把数据形成字典，传参给模板，为模板渲染提供数据
1. 使用 loader 加载模板
    ```python
    t = loader.get_template('xxx.html')
    html = t.render(字典数据)
    return HttpResponse(html)
    ```
2. 使用render加载模板
    ```python
    return render(request,'xxx.html',字典数据)
    ```

#### 模板的变量
1. 在模板中使用变量语法
    - `{{ 变量名 }}`
    - `{{ 变量名.index }}`   
    - `{{ 变量名.key}}`
    - `{{ 对象.方法 }}`
    - `{{ 函数名 }}`

    1. 视图函数中必须将变量封装到字典中才允许传递到模板上
        ```python
        def xxx_view(request)
            dic = {
                "变量1":"值1",
                "变量2":"值2",
            }
            return render(request, 'xxx.html', dic)
        ```
- 练习
    - 写一个简单的计算器页面，能够在服务端进行简单加减乘除计算
        <form action='/mycal' method='POST'>
            <input type='text' name="x" value="1">
            <select>
                <option value="add"> +加 </option>
                <option value="sub"> -减 </option>
                <option value="mul"> *乘 </option>
                <option value="div"> /除 </option>
            </select>
            <input type='text' name="y" value="2"> = <span>3</span>
            <div>
                <input type="submit" value='开始计算'>
            <div>
        </form>

    - 参考代码
        ```html
        <form action='/mycal' method='POST'>
            <input type='text' name="x" value="{{ x }}">
            <select name='op'>
                <option value="add"> +加 </option>
                <option value="sub"> -减 </option>
                <option value="mul"> *乘 </option>
                <option value="div"> /除 </option>
            </select>
            <input type='text' name="y" value="2"> = <span>3</span>
            <div>
                <input type="submit" value='开始计算'>
            <div>
        </form>
        ```


#### 模板的标签
1. 作用

    - 将一些服务器端的功能嵌入到模板中

2. 标签语法
    ```
    {% 标签 %}
    ...
    {% 结束标签 %}
    ```

3. if 标签
    ```
    {% if 条件表达式1 %}
    ...
    {% elif 条件表达式2 %}
    ...
    {% elif 条件表达式3 %}
    ...
    {% else %}
    ...
    {% endif %}
    ```

4. if 标签里的布尔运算符

    - if 条件表达式里可以用的运算符 ==, !=, <, >, <=, >=, in, not in, is, is not, not、and、or
    - 在if标记中使用实际括号是无效的语法。 如果您需要它们指示优先级，则应使用嵌套的if标记。

5. locals函数的使用

    locals() 返回当前函数作用域内全部局部变量形成的字典。

6. for 标签
    1. 语法
        ```
        {% for 变量 in 可迭代对象 %}
            ... 循环语句
        {% empty %}
            ... 可迭代对象无数据时填充的语句
        {% endfor %}
        ```
    2. 内置变量 - forloop
        |        变量         |                描述                 |
        | :-----------------: | :---------------------------------: |
        |   forloop.counter   |    循环的当前迭代（从1开始索引）    |
        |  forloop.counter0   |    循环的当前迭代（从0开始索引）    |
        | forloop.revcounter  |  循环结束的迭代次数（从1开始索引）  |
        | forloop.revcounter0 |  循环结束的迭代次数（从0开始索引）  |
        |    forloop.first    |   如果这是第一次通过循环，则为真    |
        |    forloop.last     |    如果这是最后一次循环，则为真     |
        | forloop.parentloop  | 当嵌套循环，parentloop 表示外层循环 |

    3.  遍历字典的 key 和 value

       ```python
       1,  只遍历key  
       	{% for i in dic %}
       		{{ i }}
           {% endfor %}
       
       2,  遍历 key 和 value
       	{% for k, v in dic.item %}
           	键：{{ k }}  值: {{ v }}
           {% endfor %}
       
       ```


#### 过滤器

1. 作用
    - 在变量输出时对变量的值进行处理
    - 您可以通过使用 过滤器来改变变量的输出显示。
2. 语法
   
    - {{ 变量 | 过滤器1:参数值1 | 过滤器2:参数值2 ... }}
3. 常用的过滤器
    |      过滤器       |                             说明                             |
    | :---------------: | :----------------------------------------------------------: |
    |       lower       |                   将字符串转换为全部小写。                   |
    |       upper       |                    将字符串转换为大写形式                    |
    |       safe        |              默认不对变量内的字符串进行html转义              |
    |     add: "n"      |                      将value的值增加 n                       |
    | truncatechars:'n' | 如果字符串字符多于指定的字符数量，那么会被截断。 截断的字符串将以可翻译的省略号序列（“...”）结尾。 |
    |        ...        |                                                              |

5. 文档参见:
   
    - <https://docs.djangoproject.com/en/1.11/ref/templates/builtins/>


### 模板的继承
- 模板继承可以使父模板的内容重用,子模板直接继承父模板的全部内容并可以覆盖父模板中相应的块
- 定义父模板中的块 `block`标签
    - 标识出哪些在子模块中是允许被修改的
    - block标签：在父模板中定义，可以在子模板中覆盖
        ```
        {% block block_name %}
        定义模板块，此模板块可以被子模板重新定义的同名块覆盖
        {% endblock block_name %}
        ```
- 继承模板 `extends` 标签(写在模板文件的第一行)
    - 子模板继承语法标签
        - `{% extends '父模板名称' %}`
        - 如:
            - `{% extends 'base.html' %}`
    - 子模板 重写父模板中的内容块
    ```
    {% block block_name %}
    子模板块用来覆盖父模板中 block_name 块的内容
    {% endblock block_name %}
    ```
    - 重写的覆盖规则
        - 不重写,将按照父模板的效果显示
        - 重写,则按照重写效果显示
    - 注意
        - 模板继承时,服务器端的动态内容无法继承

- 参考文档
  
- <https://docs.djangoproject.com/en/1.11/ref/templates/>
  
- 模板的继承示例:
  
    - ![](images/template_inherit.png)

### url 反向解析
- url 反向解析是指在视图或模板中，用为url定义的名称来查找或计算出相应的路由
- url 函数的语法
    - url(regex, views, kwargs=None, name="别名")
    - 例如:
        - url(r'^user_login$', views.login_view, name="login")

- url() 的`name`关键字参数
    - 作用:
      
        - 根据url 列表中的`name=`关键字传参给 url确定了个唯一确定的名字，在模板中，可以通过这个名字反向推断出此url信息
    - 在模板中通过别名实现地址的反向解析
        ```
        {% url '别名' %}
        {% url '别名' '参数值1' '参数值2' %}
        ```
- 练习:
    ```
    写一个有四个自定义页面的网站，对应路由:
    /       主页
    /page1   页面1
    /page2   页面2
    /page3   页面3
    功能: 主页加 三个页面的连接分别跳转到一个 页面，三个页面每个页面加入一个链接用于返回主页
    ```

## 静态文件

1. 什么是静态文件
    - 不能与服务器端做动态交互的文件都是静态文件
    - 如:图片,css,js,音频,视频,html文件(部分)
2. 静态文件配置
    - 在 settings.py 中配置一下两项内容:
    1. 配置静态文件的访问路径
        - 通过哪个url地址找静态文件
        - STATIC_URL = '/static/'
        - 说明:
            - 指定访问静态文件时是需要通过 /static/xxx或 127.0.0.1:8000/static/xxx
            - xxx 表示具体的静态资源位置
    2. 配置静态文件的存储路径 `STATICFILES_DIRS`
      
        - STATICFILES_DIRS保存的是静态文件在服务器端的存储位置
    3. 示例:
        ```python
        # file: setting.py
        STATICFILES_DIRS = (
            os.path.join(BASE_DIR, "static"),
        )
        ```
3. 访问静态文件
    1. 使用静态文件的访问路径进行访问
        - 访问路径: STATIC_URL = '/static/'
        -  示例:
            ```python
            <img src="/static/images/lena.jpg">
            <img src="http://127.0.0.1:8000/static/images/lena.jpg">
            ```
    2. 通过 {% static %}标签访问静态文件
        - `{% static %}` 表示的就是静态文件访问路径

        1. 加载 static
            - `{% load static %}`
        2. 使用静态资源时
            - 语法:
                - `{% static '静态资源路径' %}`
            - 示例:
                - `<img src="{% static 'images/lena.jpg' %}">`

## Django中的应用 - app
- 应用在Django项目中是一个独立的业务模块,可以包含自己的路由,视图,模板,模型

###  创建应用app
- 创建步骤
    1. 用manage.py 中的子命令 startapp 创建应用文件夹
    2. 在settings.py 的 INSTALLED_APPS 列表中配置安装此应用

- 创建应用的子命令
    - python3 manage.py startapp 应用名称(必须是标识符命令规则)
    - 如:
        - python3 manage.py startapp music

- Django应用的结构组成
    1. `migrations` 文件夹
        - 保存数据迁移的中间文件
    2. `__init__.py`
        - 应用子包的初始化文件
    3. `admin.py`
        - 应用的后台管理配置文件
    4. `apps.py`
        - 应用的属性配置文件
    5. `models.py`
        - 与数据库相关的模型映射类文件
    6. `tests.py`
        - 应用的单元测试文件
    7. `views.py`
        - 定义视图处理函数的文件

- 配置安装应用
    - 在 settings.py 中配置应用, 让此应用能和整个项目融为一体
        ```python
        # file : settings.py 
        INSTALLED_APPS = [
            ... ...,
            '自定义应用名称'
        ]

        ```
    - 如:
        ```python
        INSTALLED_APPS = [
            # ....
            'user',  # 用户信息模块
            'music',  # 收藏模块
        ]
        ```

### 应用的分布式路由
- Django中，基础路由配置文件(urls.py)可以不处理用户具体路由，基础路由配置文件的可以做请求的分发(分布式请求处理)。具体的请求可以由各自的应用来进行处理
- 127.0.0.1:8000/news/get_news/today   -> news应用下  urls.py -> get_news/today  -> 找哪个news应用下的 views.函数
- 127.0.0.1:8000/music/jielun/11111123  -> music应用下的urls.py ->......
- 如图:
    - ![](images/urls.png)
#### include 函数
- 作用:
  
    - 用于分发将当前路由转到各个应用的路由配置文件的 urlpatterns 进行分布式处理
- 函数格式
    - include('app命字.url模块名')
    > 模块`app命字/url模块名.py` 文件件里必须有urlpatterns 列表
    > 使用前需要使用 `from django.conf.urls import include` 导入此函数

- 练习:
    ```
    1.创建四个应用
        1.创建 index 应用,并注册
        2.创建 sport 应用,并注册
        3.创建 news  应用,并注册   注册即在settings.py中登记该应用
        4.创建 music 应用,并注册
    2.创建分布式路由系统
        主路由配置只做分发
        每个应用中处理具体访问路径和视图
        1. 127.0.0.1:8000/music/index
            交给 music 应用中的 index_view() 函数处理
        2. 127.0.0.1:8000/sport/index
            交给 sport 应用中的 index_view() 函数处理
        3. 127.0.0.1:8000/news/index
            交给 news  应用中的 index_view() 处理处理
    ```



注意：  

1，先创建应用 再注册应用； 否则执行 python3 manage.py startapp 应用名时 会抛出 no module named 应用名 错误

2，一定要创建完应用后 即刻注册 【settings.py 里 添加自定义应用】

3，app下可以创建应用内部的templates文件夹，该文件夹可供开发人员存储当前应用下的html ;  如果settings.py中 TEMPLATES 配置了 DIRS属性

【即配置了外部的html集中存储文件夹】, 则优先查找外部的存储文件夹，其次再查找应用内部的templates~

4，如果出现 TemplatesDoesNotExisted  则尝试重启进程 触发加载配置

5，当每个应用下都有templates时，请注意

	有可能当前应用加载了 其他应用中的 同名html
	
	解决方案： 
	
	1,app下的templates下创建同应用名的子文件夹，将该应用所有html转至该文件夹； ex: mysite3/music/templates/music/index.html
	
	2, music视图函数中， renturn render(request, 'music/index.html')



## 数据库 和 模型

### Django下配置使用 mysql 数据库
1. 安装 pymysql包
    - 用作 python 和 mysql 的接口
        - `$ sudo pip3 install pymysql`
    - 安装 mysql 客户端(非必须)
        `$ sudo pip3 install mysqlclient`

2. 创建 和 配置数据库
    1. 创建数据库
        - 创建 `create database 数据库名 default charset utf8 collate utf8_general_ci;     `
        ```sql
        create database mywebdb default charset utf8 collate utf8_general_ci;
        ```
    2. 数据库的配置
        - sqlite 数据库配置
            ```python
            # file: settings.py
            DATABASES = {
                'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                }
            }
            ```
        - mysql 数据库配置
            ```python
            DATABASES = {
                'default' : {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': 'mywebdb',  # 数据库名称,需要自己定义
                    'USER': 'root',
                    'PASSWORD': '123456',  # 管理员密码
                    'HOST': '127.0.0.1',
                    'PORT': 3306,
                }
            }
            ```
    3. 关于数据库的SETTING设置
        1. ENGINE
            - 指定数据库的后端引擎
            ```
            'django.db.backends.mysql'
            'django.db.backends.sqlite3'
            'django.db.backends.oracle'
            'django.db.backends.postgresql'
            ```
            - mysql引擎如下:
                - 'django.db.backends.mysql'

        2. NAME
            - 指定要连接的数据库的名称
            - `'NAME': 'mywebdb'`
        3. USER
            - 指定登录到数据库的用户名
            - `'USER':'root'`
        4. PASSWORD
            - 接数据库时使用的密码。
            - `'PASSWORD':'123456'`
        5. HOST
            - 连接数据库时使用哪个主机。
            - `'HOST':'127.0.0.1'`
        6. PORT
            - 连接数据库时使用的端口。
            - `'PORT':'3306'`
    3. 添加 mysql 支持
        - 安装pymysql 模块
          
            - `$ sudo pip install pymysql`
        - 修改项目中__init__.py 加入如下内容来提供pymysql引擎的支持
            ```python
            import pymysql
            pymysql.install_as_MySQLdb()
            ```

### 模型（Models）
- 模型是一个Python类，它是由django.db.models.Model派生出的子类。
- 一个模型类代表数据库中的一张数据表
- 模型类中每一个类属性都代表数据表中的一个字段。
- 模型是数据交互的接口，是表示和操作数据库的方法和方式


### Django 的 ORM框架
- ORM（Object Relational Mapping）即对象关系映射，它是一种程序技术，它允许你使用类和对象对数据库进行操作,从而避免通过SQL语句操作数据库
- ORM框架的作用
    1. 建立模型类和表之间的对应关系，允许我们通过面向对象的方式来操作数据库。
    2. 根据设计的模型类生成数据库中的表格。
    3. 通过简单的配置就可以进行数据库的切换。
- ORM 好处:
    1. 只需要面向对象编程, 不需要面向数据库编写代码.
        - 对数据库的操作都转化成对类属性和方法的操作.
        - 不用编写各种数据库的sql语句.
    2. 实现了数据模型与数据库的解耦, 屏蔽了不同数据库操作上的差异.
        - 不在关注用的是mysql、oracle...等数据库的内部细节.
        - 通过简单的配置就可以轻松更换数据库, 而不需要修改代码.
- ORM 缺点
    1. 相比较直接使用SQL语句操作数据库,有性能损失.
    2. 根据对象的操作转换成SQL语句,根据查询的结果转化成对象, 在映射过程中有性能损失.
- ORM 示意
    - ![](images/orm.png)


2. 模型示例:
    - 此示例为添加一个 bookstore_book 数据表来存放图书馆中书目信息
    - 添加一个 bookstore 的 app
        ```shell
        $ python3 manage.py startapp bookstore
        ```
    - 添加模型类并注册app
        ```python
        # file : bookstore/models.py
        from django.db import models

        class Book(models.Model):
            title = models.CharField("书名", max_length=50, default='')
            price = models.DecimalField('定价', max_digits=7, decimal_places=2, default=0.0)
        ```
    - 注册app
        ```python
        # file : setting.py
        INSTALLED_APPS = [
            ...
            'bookstore',
        ]
        ```
3. 数据库的迁移
    - 迁移是Django同步您对模型所做更改（添加字段，删除模型等） 到您的数据库模式的方式
    1. 生成或更新迁移文件
        - 将每个应用下的models.py文件生成一个中间文件,并保存在migrations文件夹中
        - `python3 manage.py makemigrations`
    2. 执行迁移脚本程序
        - 执行迁移程序实现迁移。将每个应用下的migrations目录中的中间文件同步回数据库
        - `python3 manage.py migrate`
    - 注:
      
- 每次修改完模型类再对服务程序运行之前都需要做以上两步迁移操作。
        
    - 生成迁移脚本文件`bookstore/migrations/0001_initial.py`并进行迁移
        ```shell
        $ python3 manage.py makemigrations
        $ python3 manage.py migrate
        ```

2. 编写模型类Models
    - 模型类需继承自`django.db.models.Model`
        1. Models的语法规范
            ```
            from django.db import models
            
            class 模型类名(models.Model):
                字段名 = models.字段类型(字段选项)
            ```
        > 模型类名是数据表名的一部分，建议类名首字母大写
        > 字段名又是当前类的类属性名，此名称将作为数据表的字段名
        > 字段类型用来映射到数据表中的字段的类型
        > 字段选项为这些字段提供附加的参数信息

3. 字段类型
    1. BooleanField()
        - 数据库类型:tinyint(1)
        - 编程语言中:使用True或False来表示值
        - 在数据库中:使用1或0来表示具体的值
    2. CharField()
        - 数据库类型:varchar
        - 注意:
            - 必须要指定max_length参数值
    3. DateField()
        - 数据库类型:date
        - 作用:表示日期
        - 编程语言中:使用字符串来表示具体值
        - 参数:
            - DateField.auto_now: 每次保存对象时，自动设置该字段为当前时间(取值:True/False)。
            - DateField.auto_now_add: 当对象第一次被创建时自动设置当前时间(取值:True/False)。
            - DateField.default: 设置当前时间(取值:字符串格式时间如: '2019-6-1')。
            - 以上三个参数只能多选一
    4. DateTimeField()
        - 数据库类型:datetime(6)
        - 作用:表示日期和时间
        - models.DateTimeField(auto_now_add=True,  )
        - default='2019-10-1 18:15:20'

    5. DecimalField()
        - 数据库类型:decimal(x,y)
        - 编程语言中:使用小数表示该列的值
        - 在数据库中:使用小数
        - 参数:
            - DecimalField.max_digits: 位数总数，包括小数点后的位数。 该值必须大于等于decimal_places.
            - DecimalField.decimal_places: 小数点后的数字数量

        - 示例:
            ```python
            money=models.DecimalField(
                max_digits=7,
                decimal_places=2,
                default=0.0
            )
            ```
    6. FloatField()
        - 数据库类型:double
        - 编程语言中和数据库中都使用小数表示值
    7. EmailField()  
        - 数据库类型:varchar
        - 编程语言和数据库中使用字符串
    8. IntegerField()
        - 数据库类型:int
        - 编程语言和数据库中使用整数
    9. URLField()
        - 数据库类型:varchar(200)
        - 编程语言和数据库中使用字符串
    10. ImageField()
        - 数据库类型:varchar(100)
        - 作用:在数据库中为了保存图片的路径
        - 编程语言和数据库中使用字符串
        - 示例:
            ```
            image=models.ImageField(
                upload_to="static/images"
            )
            ```
        - upload_to:指定图片的上传路径
            在后台上传时会自动的将文件保存在指定的目录下
    11. TextField()
         - 数据库类型:longtext
         - 作用:表示不定长的字符数据
    
- 参考文档 <https://docs.djangoproject.com/en/1.11/ref/models/fields/#field-types>
  
4. 字段选项FIELD_OPTIONS
    - 字段选项, 指定创建的列的额外的信息
    - 允许出现多个字段选项,多个选项之间使用,隔开
    1. primary_key
        - 如果设置为True,表示该列为主键,如果指定一个字段为主键，则此数库表不会创建id字段
    2. blank
        - 设置为True时，字段可以为空。设置为False时，字段是必须填写的。
    3. null
        - 如果设置为True,表示该列值允许为空。
        - 默认为False,如果此选项为False建议加入default选项来设置默认值
    4. default
        - 设置所在列的默认值,如果字段选项null=False建议添加此项
    5. db_index
        - 如果设置为True,表示为该列增加索引
    6. unique
        - 如果设置为True,表示该字段在数据库中的值必须是唯一(不能重复出现的)
    7. db_column
        - 指定列的名称,如果不指定的话则采用属性名作为列名
    8. verbose_name
        - 设置此字段在admin界面上的显示名称。
    - 示例:
        ```python
        # 创建一个属性,表示用户名称,长度30个字符,必须是唯一的,不能为空,添加索引
        name = models.CharField(max_length=30, unique=True, null=False, db_index=True)
        ```
- 文档参见:
    - <https://docs.djangoproject.com/en/1.11/ref/models/fields/#field-options>


### 数据库迁移的错误处理方法
- 当执行 `$ python3 manage.py makemigrations` 出现如下迁移错误时的处理方法
    - 错误信息
        ```
        $ python3 manage.py makemigrations
        You are trying to change the nullable field 'title' on book to non-nullable without a default; we can't do that (the database needs something to populate existing rows).
        Please select a fix:
        1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
        2) Ignore for now, and let me handle existing rows with NULL myself (e.g. because you added a RunPython or RunSQL operation to handle NULL values in a previous data migration)
        3) Quit, and let me add a default in models.py
        Select an option: 
        ```
    - 翻译为中文如下:
        ```
        $ python3 manage.py makemigrations
        您试图将图书上的可空字段“title”更改为非空字段(没有默认值);我们不能这样做(数据库需要填充现有行)。
        请选择修复:
        1)现在提供一次性默认值(将对所有现有行设置此列的空值)
        2)暂时忽略，让我自己处理空值的现有行(例如，因为您在以前的数据迁移中添加了RunPython或RunSQL操作来处理空值)
        3)退出，让我在models.py中添加一个默认值
        选择一个选项:
        ```
    - 错误原因
        - 当将如下代码
        ```
        class Book(models.Model):
            title = models.CharField("书名", max_length=50, null=True)
        ```
        - 去掉 null=True 改为如下内容时会出现上述错误
        ```
        class Book(models.Model):
            title = models.CharField("书名", max_length=50)
        ```
        - 原理是 此数据库的title 字段由原来的可以为NULL改为非NULL状态,意味着原来这个字段可以不填值，现在改为必须填定一个值，那填什么值呢？此时必须添加一个缺省值。
    - 处理方法:
        1. 选择1 手动给出一个缺省值，在生成 bookstore/migrations/000x_auto_xxxxxxxx_xxxx.py 文件时自动将输入的值添加到default参数中
        2. 暂时忽略，以后用其它的命令处理缺省值问题(不推荐)
        3. 退出当前生成迁移文件的过程，自己去修改models.py, 新增加一个`default=XXX` 的缺省值(推荐使用)

- 数据库的迁移文件混乱的解决办法
    1. 删除 所有 migrations 里所有的 000?_XXXX.py (`__init__.py`除外)
    2. 删除 数据表
        - sql> drop database mywebdb;
    3. 重新创建 数据表
        - sql> create datebase mywebdb default charset...;
    4. 重新生成migrations里所有的 000?_XXXX.py
        - python3 manage.py makemigrations
    5. 重新更新数据库
        - python3 manage.py migrate


## 数据库的基本操作
- 数据库的基本操作包括增删改查操作，即(CRUD操作)
- CRUD是指在做计算处理时的增加(Create)、读取查询(Read)、更新(Update)和删除(Delete)

### 管理器对象
- 每个继承自 models.Model 的模型类，都会有一个 objects 对象被同样继承下来。这个对象叫管理器对象
- 数据库的增删改查可以通过模型的管理器实现
    ```python
    class MyModel(models.Model):
        ...
    MyModel.objects.create(...) # objects 是管理器对象
    ```

### 创建数据对象
- Django 使用一种直观的方式把数据库表中的数据表示成Python 对象
- 创建数据中每一条记录就是创建一个数据对象
    1. MyModel.objects.create(属性1=值1, 属性2=值1,...)
        - 成功: 返回创建好的实体对象
        - 失败: 抛出异常
    2. 创建 MyModel 实例对象,并调用 save() 进行保存
        ```python
        obj = MyModel(属性=值,属性=值)
        obj.属性=值
        obj.save()
        无返回值,保存成功后,obj会被重新赋值
        ```

### shell 操作
- 在Django提供了一个交互式的操作项目叫 `Django Shell` 它能够在交互模式用项目工程的代码执行相应的操作
- 利用 Django Shell 可以代替编写View的代码来进行直接操作
- 在Django Shell 下只能进行简单的操作，不能运行远程调式
- 启动方式:
    ```shell
    $ python3 manage.py shell
    ```

- 练习:
    ```
    在 bookstore/models.py 应用中添加两个model类
    1. Book - 图书
        1. title - CharField 书名,非空,唯一
        2. pub - CharField 出版社,字符串,非空
        3. price - 图书定价,,
        4. market_price - 图书零售价
    2. Author - 作者
        1. name - CharField 姓名,非空
        2. age - IntegerField, 年龄,非空，缺省值为1
        3. email - EmailField, 邮箱,允许为空
    ```
    - 然后用 Django Shell 添加如下数据
        - 图书信息
            | 书名    | 定价  | 零售价  | 出版社         |
            | ------- | ----- | ------- | -------------- |
            | Python  | 20.00 | 25.00   | 清华大学出版社 |
            | Python3 | 60.00 | 65.00   | 清华大学出版社 |
            | Django  | 70.00 | 75.0  0 | 清华大学出版社 |
            | JQuery  | 90.00 | 85.00   | 机械工业出版社 |
            | Linux   | 80.00 | 65.00   | 机械工业出版社 |
            | Windows | 50.00 | 35.00   | 机械工业出版社 |
            | HTML5   | 90.00 | 105.00  | 清华大学出版社 |
        - 作者信息:
            | 姓名   | 年龄 | 邮箱                |
            | ------ | ---- | ------------------- |
            | 王老师 | 28   | wangweichao@tedu.cn |
            | 吕老师 | 31   | lvze@tedu.cn        |
            | 祁老师 | 30   | qitx@tedu.cn        |
        
## 查询数据

- 数据库的查询需要使用管理器对象进行 

- 通过 MyModel.objects 管理器方法调用查询接口

  | 方法      | 说明                              |
  | --------- | --------------------------------- |
  | all()     | 查询全部记录,返回QuerySet查询对象 |
  | get()     | 查询符合条件的单一记录            |
  | filter()  | 查询符合条件的多条记录            |
  | exclude() | 查询符合条件之外的全部记录        |
  | ...       |                                   |

1. all()方法

   - 方法: all()

   - 用法: MyModel.objects.all()

   - 作用: 查询MyModel实体中所有的数据

     - 等同于
       - select * from tabel

   - 返回值: QuerySet容器对象,内部存放 MyModel 实例

   - 示例:

     ```python
     from bookstore import models
     books = models.Book.objects.all()
     for book in books:
         print("书名", book.title, '出版社:', book.pub)
     ```

2. 在模型类中定义 `def __str__(self): ` 方法可以将
### 自定义默认字符串

   ```python
   class Book(models.Model):
       title = ...
       def __str__(self):
           return "书名: %s, 出版社: %s, 定价: %s" % (self.title, self.pub, self.price)
   ```

3. 查询返回指定列(字典表示)

   - 方法: values('列1', '列2')

   - 用法: MyModel.objects.values(...)

   - 作用: 查询部分列的数据并返回

     - select 列1,列2 from xxx

   - 返回值: QuerySet

     - 返回查询结果容器，容器内存字典，每个字典代表一条数据,
     - 格式为: {'列1': 值1, '列2': 值2}

   - 示例:

     ```python
     from bookstore import models
     books = models.Book.objects.values("title", "pub")
     for book in books:
         print("书名", book["title"], '出版社:', book['pub'])
         print("book=", book)
     ```

4. 查询返回指定列（元组表示)

   - 方法:values_list('列1','列2')

   - 用法:MyModel.objects.values_list(...)

   - 作用:

     - 返回元组形式的查询结果

   - 返回值: QuerySet容器对象,内部存放 `元组`

     - 会将查询出来的数据封装到元组中,再封装到查询集合QuerySet中

   - 示例:

     ```python
     from bookstore import models
     books = models.Book.objects.values_list("title", "pub")
     for book in books:
     print("book=", book)  # ('Python', '清华大学出版社')...
     ```

5. 排序查询

   - 方法:order_by

   - 用法:MyModel.objects.order_by('-列','列')

   - 作用:

     - 与all()方法不同，它会用SQL 语句的ORDER BY 子句对查询结果进行根据某个字段选择性的进行排序

   - 说明:

   -     默认是按照升序排序,降序排序则需要在列前增加'-'表示

   - 示例:

     ```python
     from bookstore import models
     books = models.Book.objects.order_by("price")
     for book in books:
     print("书名:", book.title, '定价:', book.price)
     ```

### filter(条件)查询

   根据条件查询多条记录

   - 方法: filter(条件)

   - 语法: 

     ```python
     MyModel.objects.filter(属性1=值1, 属性2=值2)
     ```

   - 返回值:

     - QuerySet容器对象,内部存放 MyModel 实例

   - 说明:

     - 当多个属性在一起时为"与"关系，即当`Books.objects.filter(price=20, pub="清华大学出版社")` 返回定价为20 `且` 出版社为"清华大学出版社"的全部图书

   - 示例:

     ```python
     # 查询书中出版社为"清华大学出版社"的图书
     from bookstore import models
     books = models.Book.objects.filter(pub="清华大学出版社")
     for book in books:
         print("书名:", book.title)
     
     2. 查询Author实体中id为1并且isActive为True的
         - authors=Author.objects.filter(id=1,isActive=True)
     ```

## 字段查找

- 字段查询是指如何指定SQL语句中 WHERE 子句的内容。

- 字段查询需要通过QuerySet的filter(), exclude() and get()的关键字参数指定。

- 非等值条件的构建,需要使用字段查询

- 示例:

  ```python
  # 查询作者中年龄大于30
  Author.objects.filter(age__gt=30)
  # 对应
  # SELECT .... WHERE AGE > 35;
  ```

## 查询谓词

- 每一个查询谓词是一个独立的查询功能

1. `__exact` : 等值匹配

   ```python
   Author.objects.filter(id__exact=1)
   # 等同于select * from author where id = 1
   
   ```

2. `__contains` : 包含指定值

   ```python
   Author.objects.filter(name__contains='w')
   # 等同于 select * from author where name like '%w%'
   
   ```

3. `__startswith` : 以 XXX 开始

4. `__endswith` : 以 XXX 开始

5. `__gt` : 大于指定值

   ```python
   Author.objects.filer(age__gt=50)
   # 等同于 select * from author where age > 50
   
   ```

6. `__gte` : 大于等于

7. `__lt` : 小于

8. `__lte` : 小于等于

9. `__in` : 查找数据是否在指定范围内

   - 示例

   ```python
   Author.objects.filter(country__in=['中国','日本','韩国'])
   # 等同于 select * from author where country in ('中国','日本','韩国')
   
   ```

10. `__range`: 查找数据是否在指定的区间范围内

    ```python
    # 查找年龄在某一区间内的所有作者
    Author.objects.filter(age__range=(35,50))
    # 等同于 SELECT ... WHERE Author BETWEEN 35 and 50;
    
    ```

11. 详细内容参见: <https://docs.djangoproject.com/en/1.11/ref/models/querysets/#field-lookups>

- 示例

  ```python
  MyModel.objects.filter(id__gt=4)
  # 等同于 SELECT ... WHERE id > 4;
  
  ```

- 练习:

  1. 查询Book表中price大于等于50的信息

  2. 查询Author表中姓王的人的信息

  3. 查询Author表中Email中包含"wc"的人的信息

      

2. 不等的条件筛选

   - 语法:
     MyModel.objects.exclude(条件)

   - 作用:

     - 返回不包含此 `条件` 的 全部的数据集

   - 示例:

     - 查询 `清华大学出版社，定价大于50` 以外的全部图书

     ```python
     books = models.Book.objects.exclude(pub="清华大学出版社", price__gt=50)
     for book in books:
         print(book)
     
     ```

3. 查询指定的一条数据

   - 语法:
     MyModel.objects.get(条件)

   - 作用：

     - 返回满足条件的唯一一条数据

   - 返回值:

     - MyModel 对象

   - 

   - 说明:

     - 该方法只能返回一条数据
     - 查询结果多余一条数据则抛出,Model.MultipleObjectsReturned异常
     - 查询结果如果没有数据则抛出Model.DoesNotExist异常

   - 示例:

     ```python
     from bookstore import models
     book = models.Book.objects.get(id=1)
     print(book.title)
     
     ```

### 修改数据记录

1. 修改单个实体的某些字段值的步骤:

   1. 查
      - 通过 get() 得到要修改的实体对象
   2. 改
      - 通过 对象.属性 的方式修改数据
   3. 保存
      - 通过 对象.save() 保存数据

   - 如:

     ```python
     from bookstore import models
     abook = models.Book.objects.get(id=10)
     abook.market_price = "10.5"
     abook.save()
     
     ```

2. 通过 QuerySet 批量修改 对应的全部字段

   - 直接调用QuerySet的update(属性=值) 实现批量修改

   - 如:

     ```python
     # 将 id大于3的所有图书价格定为0元
     books = Book.objects.filter(id__gt=3)
     books.update(price=0)
     # 将所有书的零售价定为100元
     books = Book.objects.all()
     books.update(market_price=100)
     
     ```

练习：修改图书得零售价

路由：	/bookstore/mod/5



### 删除记录

- 删除记录是指删除数据库中的一条或多条记录
- 删除单个MyModel对象或删除一个查询结果集(QuerySet)中的全部对象都是调用 delete()方法

1. 删除单个对象

   - 步骤

     1. 查找查询结果对应的一个数据对象
     2. 调用这个数据对象的delete()方法实现删除

   - 示例:

     ```python
     try:
         auth = Author.objects.get(id=1)
         auth.delete()
     except:
         print(删除失败)
     
     ```

2. 删除查询结果集

   - 步骤

     1. 查找查询结果集中满足条件的全部QuerySet查询集合对象
     2. 调用查询集合对象的delete()方法实现删除

   - 示例:

     ```python
     # 删除全部作者中，年龄大于65的全部信息
     auths = Author.objects.filter(age__gt=65)
     auths.delete()
     
     ```

### 聚合查询

- 聚合查询是指对一个数据表中的一个字段的数据进行部分或全部进行统计查询,查bookstore_book数据表中的全部书的平均价格，查询所有书的总个数等,都要使用聚合查询

#### 不带分组

- 不带分组的聚合查询是指导将全部数据进行集中统计查询

- 聚合函数:

  - 定义模块: `django.db.models`
  - 用法: `from django.db.models import *`
  - 聚合函数: 
    - Sum, Avg, Count, Max, Min

- 语法: 

  - MyModel.objects.aggregate(结果变量名=聚合函数('列'))

- 返回结果:

  - 由 结果变量名和值组成的字典
  - 格式为:
    - `{"结果变量名": 值}

- 示例:

  ```python
  # 得到所有书的平均价格
  from bookstore import models
  from django.db.models import Count
  result = models.Book.objects.aggregate(myAvg=Avg('price'))
  print("平均价格是:", result['myAvg'])
  print("result=", result)  # {"myAvg": 58.2}
  
  # 得到数据表里有多少本书
  from django.db.models import Count
  result = models.Book.objects.aggregate(mycnt=Count('title'))
  print("数据记录总个数是:", result['mycnt'])
  print("result=", result)  # {"mycnt": 10}
  
  
  ```

#### 分组聚合

- 分组聚合是指通过计算查询结果中每一个对象所关联的对象集合，从而得出总计值(也可以是平均值或总和)，即为查询集的每一项生成聚合。

- 语法: 

  - QuerySet.annotate(结果变量名=聚合函数('列'))

- 用法步骤:

  1. 通过先用查询结果MyModel.objects.value. 查找查询要分组聚合的列

     - MyModel.objects.value('列1', '列2')

     - 如: 

       ```python
       pub_set = models.Book.objects.values('pub')
       print(books)  # <QuerySet [{'pub': '清华大学出版社'}, {'pub': '清华大学出版社'}, {'pub_hou {'pub': '机械工业出版社'}, {'pub': '清华大学出版社'}]>
       
       
       ```

  2. 通过返回结果的 QuerySet.annotate 方法分组聚合得到分组结果

     - QuerySet.annotate(名=聚合函数('列'))

     - 返回 QuerySet 结果集,内部存储结果的字典

     - 如:

       ```python
       pub_count_set = pub_set.annotate(myCount=Count('pub'))
       print(pub_count_set)  # <QuerySet [{'pub': '清华大学出版社', 'myCount': 7}, {'pub': '机械工业出版社', 'myCount': 3}]>
       
       ```

  - .values('查询列名')

- 示例:

  - 得到哪儿个出版社共出版多少本书

  ```python
  def test_annotate(request):
     from django.db.models import Count
     from . import models
  
      # 得到所有出版社的查询集合QuerySet
      pub_set = models.Book.objects.values('pub')
      # 根据出版社查询分组，出版社和Count的分组聚合查询集合
      pub_count_set = pub_set.annotate(myCount=Count('pub'))  # 返回查询集合
      for item in pub_count_set:
          print("出版社:", item['pub'], "图书有：", item['myCount'])
      return HttpResponse('请查看服务器端控制台获取结果')
  
  ```

### F对象

- 一个F对象代表数据库中某条记录的字段的信息

1. 作用:

   - 通常是对数据库中的字段值在不获取的情况下进行操作
   - 用于类属性(字段)之间的比较。

2. 用法

   - F对象在数据包 django.db.models 中，使用时需要先导入
     - `from django.db.models import F`

3. 语法:

   ```python
   from django.db.models import F
   F('列名')
   
   ```

4. 说明:

   - 一个 F() 对象代表了一个model的字段的值
   - F对象通常是对数据库中的字段值在不加载到内存中的情况下直接在数据库服务器端进行操作



5. 示例1

   - 更新Book实例中所有的零售价涨10元

   ```python
   models.Book.objects.all().update(market_price=F('market_price')+10)
   # 以下做法好于如下代码
   books = models.Book.objects.all()
   for book in books:
       book.update(market_price=book.marget_price+10)
       book.save()
   
   ```

6. 示例2

   - 对数据库中两个字段的值进行比较，列出哪儿些书的零售价高于定价?

   ```python
   from django.db.models import F
   from bookstore import models
   books = models.Book.objects.filter(market_price__gt=F('price'))
   for book in books:
       print(book.title, '定价:', book.price, '现价:', book.market_price)
   
   ```

### Q对象 - Q()

- 当在获取查询结果集 使用复杂的逻辑或  `|` 、 逻辑非 `~` 等操作时可以借助于 Q对象进行操作

- 如: 想找出定价低于20元 或 清华大学出版社的全部书，可以写成

  ```python
  models.Book.objects.filter(Q(price__lt=20)|Q(pub="清华大学出版社"))
  
  ```

- Q对象在 数据包 django.db.models 中。需要先导入再使用

  - `from django.db.models import Q`

1. 作用

   - 在条件中用来实现除 and(&) 以外的 or(|) 或 not(~) 操作

2. 运算符:

   - & 与操作
   - | 或操作
   - 〜 非操作

3. 语法

   ```python
   from django.db.models import Q
   Q(条件1)|Q(条件2)  # 条件1成立或条件2成立
   Q(条件1)&Q(条件2)  # 条件1和条件2同时成立
   Q(条件1)&~Q(条件2)  # 条件1成立且条件2不成立
   ...
   
   ```

4. 示例

   ```python
   from django.db.models import Q
   # 查找清华大学出版社的书或价格低于50的书
   models.Book.objects.filter(Q(market_price__lt=50) | Q(pub_house='清华大学出版社'))
   # 查找不是机械工业出版社的书且价格低于50的书
   models.Book.objects.filter(Q(market_price__lt=50) & ~Q(pub_house='机械工业出版社'))
   
   ```

### 原生的数据库操作方法

- 使用MyModel.objects.raw()进行 数据库查询操作查询

  - 在django中，可以使用模型管理器的raw方法来执行select语句进行数据查询

  1. 语法: 

     - `MyModel.objects.raw(sql语句)`
  2. 用法

     - `MyModel.objects.raw('sql语句')`
  3. 返回值:

     - QuerySet 集合对象

4. 示例

   ```python
   books = models.Book.objects.raw('select * from bookstore_book')
   
   ```

for book in books:
        print(book)
    ```

- 使用django中的游标cursor对数据库进行 增删改操作

  - 在Django中可以使用 如UPDATE,DELETE等SQL语句对数据库进行操作。

  - 在Django中使用上述非查询语句必须使用游标进行操作

  - 使用步骤:

    1. 导入cursor所在的包

       - Django中的游标cursor定义在 django.db.connection包中，使用前需要先导入
       - 如：
         - `from django.db import connection`

    2. 用创建cursor类的构造函数创建cursor对象，再使用cursor对象,为保证在出现异常时能释放cursor资源,通常使用with语句进行创建操作

       - 如:

         ```python
         from django.db import connection
         with connection.cursor() as cur:
             cur.execute('执行SQL语句')
         ```

    - 示例

      ```python
      # 用SQL语句将id 为 10的 书的出版社改为 "XXX出版社"
      from django.db import connection
      with connection.cursor() as cur: 
          cur.execute('update bookstore_book set pub_house="XXX出版社" where id=10;')
      
      with connection.cursor() as cur:
          # 删除 id为1的一条记录
          cur.execute('delete from bookstore_book where id=10;')
      ```

## admin 后台数据库管理

- django 提供了比较完善的后台管理数据库的接口，可供开发过程中调用和测试使用

- django 会搜集所有已注册的模型类，为这些模型类提拱数据管理界面，供开发者使用

- 使用步骤:

  1. 创建后台管理帐号:

     - 后台管理--创建管理员帐号

       - `$ python3 manage.py createsuperuser`            
       - 根据提示完成注册,参考如下:

       ```shell
       $ python3 manage.py createsuperuser
       Username (leave blank to use 'tarena'): guoxiaonao  # 此处输入用户名
       Email address: laowei@tedu.cn  # 此处输入邮箱
       Password: guoxiaonao # 此处输入密码(密码要复杂些，否则会提示密码太简单)
       Password (again): guoxiaonao # 再次输入重复密码
       Superuser created successfully.
       $ 
       ```

  2. 用注册的帐号登陆后台管理界面

     - 后台管理的登录地址:
       - <http://127.0.0.1:8000/admin>

### 自定义后台管理数据表

- 若要自己定义的模型类也能在 `/admin` 后台管理界中显示和管理，需要将自己的类注册到后台管理界面

- 添加自己定义模型类的后台管理数据表的,需要用`admin.site.register(自定义模型类)` 方法进行注册

  - 配置步骤如下:

    1. 在应用app中的admin.py中导入注册要管理的模型models类, 如:

       ```python
       from . import models
       ```

    2. 调用 admin.site.register 方法进行注册,如:

       ```python
       from django.contrib import admin
       admin.site.register(自定义模型类)
       ```

  - 如: 在 bookstore/admin.py 添加如下代码对Book类进行管理

  - 示例:

    ```python
    # file: bookstore/admin.py
    from django.contrib import admin
    # Register your models here.
    
    from . import models
    ...
    admin.site.register(models.Book)  # 将Book类注册为可管理页面
    ```

### 后台Models的展现形式

- 在admin后台管理数据库中对自定义的数据记录都展示为 `XXXX object` 类型的记录，不便于阅读和判断

- 在用户自定义的模型类中可以重写 `def __str__(self):` 方法解决显示问题,如:

  - 在 自定义模型类中重写 __str__(self) 方法返回显示文字内容:

  ```python
  class Book(models.Model):
      ...
      def __str__(self):
          return "书名" + self.title
  ```

### 模型管理器类

- 作用:

  - 为后台管理界面添加便于操作的新功能。

- 说明:

  - 后台管理器类须继承自 `django.contrib.admin` 里的 `ModelAdmin` 类

- 模型管理器的使用方法:

  1. 在 `<应用app>/admin.py` 里定义模型管理器类

     ```python
     class XXXX_Manager(admin.ModelAdmin):
         ......
     ```

  2. 注册管理器与模型类关联

     ```python
     from django.contrib import admin
     from . import models
     admin.site.register(models.YYYY, XXXX_Manager) # 注册models.YYYY 模型类与 管理器类 XXXX_Manager 关联
     ```

  - 示例:

    ```python
    # file : bookstore/admin.py
    from django.contrib import admin
    from . import models
    
    class BookAdmin(admin.ModelAdmin):
        list_display = ['id', 'title', 'price', 'market_price']
    
    admin.site.register(models.Book, BookAdmin)
    ```

    - 进入<http://127.0.0.1:8000/admin/bookstore/book/> 查看显示方式和以前有所不同

- 模型管理器类ModelAdmin中实现的高级管理功能

  1. list_display 去控制哪些字段会显示在Admin 的修改列表页面中。
  2. list_display_links 可以控制list_display中的字段是否应该链接到对象的“更改”页面。
  3. list_filter 设置激活Admin 修改列表页面右侧栏中的过滤器
  4. search_fields 设置启用Admin 更改列表页面上的搜索框。 
  5. list_editable 设置为模型上的字段名称列表，这将允许在更改列表页面上进行编辑。
  6. 其它参见<https://docs.djangoproject.com/en/1.11/ref/contrib/admin/>

### 数据库表管理

1. 修改模型类字段的显示名字

   - 模型类各字段的第一个参数为 verbose_name,此字段显示的名字会在后台数据库管理页面显示

   - 通过 verbose_name 字段选项,修改显示名称示例如下：

     ```python
     title = models.CharField(
         max_length = 30,
         verbose_name='显示名称'
     )
     
     ```

2. 通过Meta内嵌类 定义模型类的属性及展现形式

   - 模型类可以通过定义内部类class Meta 来重新定义当前模型类和数据表的一些属性信息

   - 用法格式如下:

     ```python
     class Book(models.Model):
         title = CharField(....)
         class Meta:
             1. db_table = '数据表名'
                 - 该模型所用的数据表的名称。(设置完成后需要立马更新同步数据库)
                 python3 manage.py makemigrations
                 python3 manage.py migrate
                 
             2. verbose_name = '单数名'
                 - 给模型对象的一个易于理解的名称(单数),用于显示在/admin管理界面中
             3. verbose_name_plural = '复数名'
                 - 该对象复数形式的名称(复数),用于显示在/admin管理界面中
     
     ```

- 练习:
  - 将Book模型类 和 Author 模型类都加入后台管理
  
  - 制作一个AuthorManager管理器类，让后台管理Authors列表中显示作者的ID、姓名、年龄信息
  
    files:admin.py里添加管理类
  
    ```
    class AuthorManager(admin.ModelAdmin):
        list_display = ['id', 'name', 'age'] #控制哪些字段显示在列表页面
        list_display_links = ['name'] #将‘title’字段链接到“更改”页面
        list_filter = ['age'] # 激活列表右侧过滤器
        search_fields = ['name','age'] #启用列表页面上方搜索框
        list_editable = ['age']  #允许在列表页面上修改
    admin.site.register(Author,AuthorManager)
    ```
  
  - 将bookstore_author 表名称改为myauthor (需要重新迁移数据库)
  
  
  files:bookstore/models.py
  
  ```
  class Author(models.Model):
        name=models.CharField(max_length=11,verbose_name='姓名')
        age=models.IntegerField(default=1,verbose_name='年龄')
        email=models.EmailField(null=True,verbose_name='邮箱')
        def __str__(self):
          return '<%s,%s,%s>' % (self.name,self.age,self.email)
          
          
        class Meta:
          # 当前model类对应的数据表表名
            db_table='author'
          verbose_name='myauthor'
            verbose_name_plural=verbose_name
  
  
  ```
  
  
  

## 数据表关联关系映射

- 在关系型数据库中，通常不会把所有数据都放在同一张表中，这样做会额外占用内存空间，
- 在关系列数据库中通常用表关联来解决数据库。
- 常用的表关联方式有三种:
  1. 一对一映射
     - 如: 一个身份证对应一个人
  2. 一对多映射  A(一)    B(多)
     - 如: 一个班级可以有多个学生
  3. 多对多映射 
     - 如: 一个学生可以报多个课程，一个课程可以有多个学生学习

### 一对一映射

- 一对一是表示现实事物间存在的一对一的对应关系。
- 如:一个家庭只有一个户主，一个男人有一个妻子，一个人有一个唯一的指纹信息等

1. 语法

   ```python
   class A(model.Model):
       ...
   
   class B(model.Model):
       属性 = models.OneToOneField(A)
   
   ```

2. 用法示例

   1. 创建作家和作家妻子类

      ```python
      # file : xxxxxxxx/models.py
      from django.db import models
      
      class Author(models.Model):
          '''作家模型类'''
          name = models.CharField('作家', max_length=50)
      
      class Wife(models.Model):
          '''作家妻子模型类'''
          name = models.CharField("妻子", max_length=50)
          author = models.OneToOneField(Author)  # 增加一对一属性
      
      ```

   2. 查询

      - 在 Wife 对象中,通过 author 属性找到对应的author对象
      - 在 Author 对象中,通过 wife 属性找到对应的wife对象

   3. 创始一对一的数据记录

      ```python
      from oto.models import Author,Wife
      author1 = Author.objects.create(name='王老师')
      wife1 = Wife.objects.create(name='王夫人', author=author1)  # 关联王老师
      author2 = Author.objects.create(name='小泽老师')  # 一对一可以没有数据对应的数据 
      
      ```

   4. 一对一数据的相互获取

      1. 正向查询

         - 直接通过关联属性查询即可

         ```python
         # 通过 wife 找 author
         from oto.models import Author,Wife
         wife = Wife.objects.get(name='王夫人')
         print(wife.name, '的老公是', wife.author.name)
         
         ```

      2. 反向查询

         - 通过反向关联属性查询
         - 反向关联属性为`实例对象.引用类名(小写)`，如作家的反向引用为`作家对象.wife`
         - 当反向引用不存在时，则会触发异常

         ```python
         # 通过 author.wife 关联属性 找 wife,如果没有对应的wife则触发异常
         from oto.models import Author,Wife
         
         author1 = Author.objects.get(name='王老师')
         print(author1.name, '的妻子是', author1.wife.name)
         author2 = Author.objects.get(name='小泽老师')
         try:
             print(author2.name, '的妻子是', author2.wife.name)
         except:
             print(author2.name, '还没有妻子')
         
         ```

- 作用:
  - 主要是解决常用数据不常用数据的存储问题,把经常加载的一个数据放在主表中，不常用数据放在另一个副表中，这样在访问主表数据时不需要加载副表中的数据以提高访问速度提高效率和节省内存空间,如经常把书的内容和书名建成两张表，因为在网站上经常访问书名等信息，但不需要得到书的内容。
- 练习:
  1. 创建一个Wife模型类,属性如下
     1. name 
     2. age 
  2. 在Wife类中增加一对一关联关系,引用 Author
  3. 同步回数据库并观察结果

### 一对多映射

- 一对多是表示现实事物间存在的一对多的对应关系。
- 如:一个学校有多个班级,一个班级有多个学生, 一本图书只能属于一个出版社,一个出版社允许出版多本图书

1. 用法语法

   - 当一个A类对象可以关联多个B类对象时

   ```python
   class A(model.Model):   一
       ...
   
   class B(model.Model):   多
       属性 = models.ForeignKey(多对一中"一"的模型类, ...)
   
   ```

2. 外键类ForeignKey 

   主表有数据   

   从表1  CASCADE - 主表删/更新数据，从表也跟着删除/更新数据

   从表2   强硬版 -  如果从表有主表想动的数据，则主表不能修改或删除

   从表3   SET NULL- 主表删除/更新 ， 从表外键变为 NULL



```
- 构造函数:
    ```python
    ForeignKey(to, on_delete, **options)
```
- 常用参数:
    - on_delete
        1. models.CASCADE  级联删除。 Django模拟SQL约束ON DELETE CASCADE的行为，并删除包含ForeignKey的对象。

           ```python
           mysql 里面 依旧还是 强硬版
           django  A主id=1   B从-f_id=1
           A想删除 id=1 数据； django先帮您把从表数据删除，再回来删除主表的数据
           ```

        2. models.PROTECT 抛出ProtectedError 以阻止被引用对象的删除;

        3. SET_NULL 设置ForeignKey null；需要指定null=True

        4. SET_DEFAULT  将ForeignKey设置为其默认值；必须设置ForeignKey的默认值。

        5. ... 其它参请参考文档 <https://docs.djangoproject.com/en/1.11/ref/models/fields/#foreignkey> ForeignKey部分
    - `**options` 可以是常用的字段选项如:

        1. null
        2. unique等
        3. ...

```

3. 示例

   - 有二个出版社对应五本书的情况.
     1. `清华大学出版社` 有书
        1. C++
        2. Java
        3. Python
     2. `北京大学出版社` 有书
        1. 西游记
        2. 水浒

   1. 定义一对多类

      ```python
      # file: one2many/models.py
      from django.db import models
      class Publisher(models.Model):
          '''出版社'''
          name = models.CharField('名称', max_length=50, unique=True)
      
      class Book(models.Model):
          title = models.CharField('书名', max_length=50)
          publisher = models.ForeignKey(Publisher, null=True)
      
      
```

   - 创建一对多的对象

     ```python
     # file: xxxxx/views.py
     from otm.models import Publisher,Book
     
     pub1 = Publisher.objects.create(name='清华大学出版社')
     Book.objects.create(title='C++', publisher=pub1)
     Book.objects.create(title='Java', publisher=pub1)
     Book.objects.create(title='Python', publisher=pub1) 
     
     pub2 = Publisher.objects.create(name='北京大学出版社')
     Book.objects.create(title='西游记', publisher=pub2)
     Book.objects.create(title='水浒', publisher=pub2)
     
     ```

   - 查询:

     - 通过多查一

     ```python
     # 通过一本书找到对应的出版社
     abook = Book.objects.get(id=1)
     print(abook.title, '的出版社是:', abook.publisher.name)
     
     ```

     - 通过一查多

     ```python
     # 通过出版社查询对应的书
     pub1 = Publisher.objects.get(name='清华大学出版社')
     books = pub1.book_set.all()  # 通过book_set 获取pub1对应的多个Book数据对象
     # books = models.Book.objects.filter(publisher=pub1)  # 也可以采用此方式获取
     print("清华大学出版社的书有:")
     for book in books:
         print(book.title)
     
     ```

- 练习:
  1. 完成Book 和 Publisher 之间的一对多
  2. 查看数据库效果
  3. 登录到后台,查看Book实体

3. 数据查询

   1. 通过 Book 查询 Publisher

      ```
      通过 publisher 属性查询即可
      练习:
          查询 西游记 对应的出版社信息,打印在终端上
      
      ```

   2. 通过 Publisher 查询 对应的所有的 Books

      ```
      Django会在Publisher中增加一个属性来表示对对应的Book们的查询引用
      属性:book_set(MyModel.objects)
      
      ```

### 多对多映射

- 多对多表达对象之间多对多复杂关系，如: 每个人都有不同的学校(小学，初中，高中,...),每个学校都有不同的学生...

1. 语法

   - 在关联的两个类中的任意一个类中,增加:

   ```python
   属性 = models.ManyToManyField(MyModel)
   
   ```

2. 示例

   - 一个作者可以出版多本图书
   - 一本图书可以被多名作者同时编写

   ```python
   class Author(models.Model):
       ...
   
   class Book(models.Model):
       ...
       authors = models.ManyToManyField(Author)
   
   ```

3. 数据查询

   1. 通过 Book 查询对应的所有的 Authors

      ```python
      book.authors.all() -> 获取 book 对应的所有的author的信息
      book.authors.filter(age__gt=80) -> 获取book对应的作者中年龄大于80岁的作者的信息
      
      ```

   2. 通过 Author 查询对应的所有的Books

      - Django会生成一个关联属性 book_set 用于表示对对应的book的查询对象相关操作

      ```python
      author.book_set.all()
      author.book_set.filter()
      author.book_set.create(...)  # 创建新书并联作用author
      author.book_set.add(book)   # 添加已有的书为当前作者author
      author.book_set.clear()  # 删除author所有并联的书
      
      ```

4. 示例:

   - 多对多模型

   ```python
   class Author(models.Model):
       '''作家模型类'''
       name = models.CharField('作家', max_length=50)
       def __str__(self):
           return self.name
   class Book(models.Model):
       title = models.CharField('书名', max_length=50)
       author = models.ManyToManyField(Author)
       def __str__(self):
           return self.title
   
   ```

   - 多对多视图操作

   ```python
   from django.http import HttpResponse
   from mtm.models import models
   
   def many2many_init(request):
       # 创建两人个作者
       author1 = Author.objects.create(name='吕泽')
       author2 = Author.objects.create(name='王老师')
   
       # 吕择和王老师同时写了一本Python
       book11 = author1.book_set.create(title="Python")
       author2.book_set.add(book11)  #
   
       # 王老师还写了两本书
       book21 = author2.book_set.create(title="C")  # 创建一本新书"C"  
       book22 = author2.book_set.create(title="C++")  # 创建一本新书"C++"
   
       return HttpResponse("初始化成功")
   
   def show_many2many(request):
       authors = Author.objects.all()
       for auth in authors:
           print("作者:", auth.name, '发出版了', auth.book_set.count(), '本书: ')
           for book in books:
               print('    ', book.title)
       print("----显示书和作者的关系----")
       books = Book.objects.all()
       for book in books:
           auths = book.author.all()
           print(book.title, '的作者是:', '、'.join([str(x.name) for x in auths]))
       return HttpResponse("显示成功，请查看服务器端控制台终端")
   ```
   
- 多对多最终的SQL结果
  
```sql
   mysql> select * from many2many_author;
   +----+-----------+
   | id | name      |
   +----+-----------+
   | 11 | 吕泽      |
   | 12 | 王老师    |
   +----+-----------+
   2 rows in set (0.00 sec)
   
   mysql> select * from many2many_book;
   +----+--------+
   | id | title  |
   +----+--------+
   | 13 | Python |
   | 14 | C      |
   | 15 | C++    |
   +----+--------+
   3 rows in set (0.00 sec)
   
   mysql> select * from many2many_book_author;
   +----+---------+-----------+
   | id | book_id | author_id |
   +----+---------+-----------+
   | 17 |      13 |        11 |
   | 20 |      13 |        12 |
   | 18 |      14 |        12 |
   | 19 |      15 |        12 |
   +----+---------+-----------+
   4 rows in set (0.00 sec)
```

## cookies 和 session

### 两者区别

  1、Cookie和Session都是会话技术，Cookie是运行在客户端，Session是运行在服务器端。

  2、Cookie有大小限制以及浏览器在存cookie的个数也有限制，Session是没有大小限制和服务器的内存大小有关。

  3、Cookie有安全隐患，通过拦截或本地文件找得到你的cookie后可以进行攻击。

  4、cookie的生命周期很长，而session很短，一般也就几十分钟。如果session过多会增加服务器的压力。

### 结合保存登录状态主题思想

1.检查登录状态思想

​	1.优先检查session

​	2.session没有数据，检查cookies，cooKies没有数据 则会写session

​	3.cookies没有数据，则让用户去登录页面

2.登录状态存储思想

​	1.肯定要存session，username，uid

​	2.按需去存cookies,【根据用户是否勾选保存密码/下次免密登录决定】

### cookies 

#### 作用

1.保持会话状态  

2.购物车 - 未登录状态下的购物记录

3.搜索引擎 - 记录当前您的搜索记录

#### 缺点

1.数据存储在客户/用户端

2.每次请求网站，自动提交当前网站的cookie,

3.网络带宽

#### 三大特点

1.存在浏览器

2.按域名隔离存储，并且是key-value 形式，且每个key都带有过期时间[回话/时间UTC]

3.自动提交。每个请求按域名发送当前域名下的所有Cookies

注意：Cookies不要存储敏感数据-密码

#### cookies概述

- cookies是保存在客户端浏览器上的存储空间，通常用来记录浏览器端自己的信息和当前连接的确认信息

- cookies 在浏览器上是以键-值对的形式进行存储的，键和值都是以ASCII字符串的形存储(不能是中文字符串)

- cookies 的内部的数据会在每次访问此网址时都会携带到服务器端，如果cookies过大会降低响应速度

- 在Django 服务器端来设置 设置浏览器的COOKIE 必须通过 HttpResponse 对象来完成

#### 存储cookie

  - 添加、修改COOKIE
    - HttpResponse.set_cookie(key, value='', max_age=None, expires=None)
      - key:cookie的名字
      - value:cookie的值
      - max_age:cookie存活时间，秒为单位
      - expires:具体过期时间
      - 当不指定max_age和expires 时,关闭浏览器时此数据失效
  - 删除COOKIE
    - HttpResponse.delete_cookie(key)
    - 删除指定的key 的Cookie。 如果key 不存在则什么也不发生。

- Django中使用

  - 使用 响应对象HttpResponse 等 将cookie保存进客户端

    1. 方法1

       ```python
       from django.http import HttpResponse
       resp = HttpResponse()
       resp.set_cookie('cookies名', cookies值, 超期时间)
       ```

       - 如:

       ```python
       resp = HttpResponse()
       resp.set_cookie('myvar', "weimz", 超期时间)
       ```

    2. 方法二, 使用render对象

       ```python
       from django.shortcuts import render
       resp = render(request,'xxx.html',locals())
       resp.set_cookie('cookies名', cookies值, 超期时间)
       ```

  #### 获取cookie

  - 通过 request.COOKIES 绑定的字典(dict) 获取客户端的 COOKIES数据

    ```python
    value = request.COOKIES.get('cookies名', '没有值!')
    print("cookies名 = ", value)
    ```

  4. 注:

     - Chrome 浏览器 可能通过开发者工具的 `Application` >> `Storage` >> `Cookies` 查看和操作浏览器端所有的 Cookies 值

- cookies 示例

  - 以下示例均在视图函数中调用

  - 添加cookie

    ```python
    # 为浏览器添加键为 my_var1,值为123，过期时间为1个小时的cookie
    responds = HttpResponse("已添加 my_var1,值为123")
    responds.set_cookie('my_var1', 123, 3600)
    return responds
    ```

  - 修改cookie

    ```python
    # 为浏览器添加键为 my_var1,修改值为456，过期时间为2个小时的cookie
    responds = HttpResponse("已修改 my_var1,值为456")
    responds.set_cookie('my_var1', 456, 3600*2)
    return responds
    ```

  - 删除cookie

    ```python
    # 删除浏览器键为 my_var1的cookie
    responds = HttpResponse("已删除 my_var1")
    responds.delete_cookie('my_var1')
    return responds
    ```

#### 获取cookie

    ```python
    # 获取浏览器中 my_var变量对应的值
    value = request.COOKIES.get('my_var1', '没有值!')
    print("cookie my_var1 = ", value)
    return HttpResponse("my_var1:" + value)
    ```

- 综合练习:

  - 实现用户注册功能，界面如下:

    - 注册界面
      - ![](images/reg.png)

  - 要求 ：

    1. 创建一个 user 应用 实现注册逻辑,如:
       - `python3 manage.py startapp user`
    2. 如果用户注册成功，则用当前浏览器的cookies记录当前成功注册的用名名
    3. 注册时如果用户输入数据合法，则在数据库记中记录用户的用户名密码等数据

  - 模型类

    1. 用户模型类

       ```python
       class User(models.Model):
           username = models.CharField("用户名", max_length=30, unique=True)
           password = models.CharField("密码", max_length=30)
       
           def __str__(self):
               return "用户" + self.username
       ```

  - 登陆设计规范(在user应用中写代码)

    | 路由正则  | 视图函数               | 模板位置                     | 说明     |
    | --------- | ---------------------- | ---------------------------- | -------- |
    | /user/reg | def reg_view(request): | templates/user/register.html | 用户注册 |



### session

#### 作用

存储会话状态-登录状态

#### 缺点

单表【点】问题

#### 单表问题 

django所有session数据存储在单个表中，表名为django_session;  并且该表没有自动回收【过期的session】，

可执行python3 manage.py clearsessions 命令进行 过期session的删除

#### session概述

- session又名会话控制，是在服务器上开辟一段空间用于保留浏览器和服务器交互时的重要数据，保持会话状态  

- session的起源

  - http协议是无状态的：每次请求都是一次新的请求，不会记得之前通信的状态
  - 实现状态保持的方式：在客户端或服务器端存储与会话有关的数据
  - 推荐使用sesison方式，所有数据存储在服务器端

- 实现方式

  - 使用 session 需要在浏览器客户端启动 cookie，且用在cookie中存储sessionid
  - 每个客户端都可以在服务器端有一个独立的Session
  - 注意：不同的请求者之间不会共享这个数据，与请求者一一对应

- Django启用Session

  - 在 settings.py 文件中

  - 向 INSTALLED_APPS 列表中添加：

    ```python
    INSTALLED_APPS = [
        # 启用 sessions 应用 33行
        'django.contrib.sessions',
    ]
    ```

  - 向 MIDDLEWARE_CLASSES 列表中添加：

    ```python
    MIDDLEWARE = [
        # 启用 Session 中间件
        'django.contrib.sessions.middleware.SessionMiddleware',
    ]
    ```

- session的基本操作:

  - session对于象是一个在似于字典的SessionStore类型的对象, 可以用类拟于字典的方式进行操作
  
- session 只能够存储能够序列化的数据,如字典，列表等。
  
#### 保存session    

  - `request.session['KEY'] = VALUE`
  - 清除：python3 manage.py clearsessions

#### 获取session

     - `VALUE = request.session['KEY']`
     - `VALUE = request.session.get('KEY', 缺省值)`

  - 删除session的值
    - `del request.session['KEY']`
  - 在 settings.py 中有关 session 的设置
    1. SESSION_COOKIE_AGE
       - 作用: 指定sessionid在cookies中的保存时长(默认是2周)，如下:
       - `SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2`
    2. SESSION_EXPIRE_AT_BROWSER_CLOSE = True
       设置只要浏览器关闭时,session就失效(默认为False)
  - session 缺省配置
    - 模块
      - `import django.conf.global_settings`

- 注: 当使用session时需要迁移数据库,否则会出现错误



## 网络云笔记项目

- 功能:
  1. 注册
  1. 登陆
  1. 退出登陆
  1. 查看笔记列表
  1. 创建新笔记
  1. 修改笔记
  1. 删除笔记

### 数据库设计

- 模型类

  1. 用户模型类

     ```python
     class User(models.Model):
         username = models.CharField("用户名", max_length=30, unique=True)
         password = models.CharField("密码", max_length=30)
     create_time = models.DateTimeField('创建时间', auto_now_add=True)
     
         def __str__(self):
             return "用户" + self.username
     ```

  2. 笔记模型类

  
      from django.db import models
      from user.models import User
        
      class Note(models.Model):
        title = models.CharField('标题', max_length=100)
          content = models.TextField('内容')
          create_time = models.DateTimeField('创建时间', auto_now_add=True)
          mod_time = models.DateTimeField('修改时间', auto_now=True)
      user = models.ForeignKey(User)
      	isActive=models.BooleanField('是否激活',default=True)

### 设计规范

- 登陆设计规范(在user应用中写代码)

  | 路由正则     | 视图函数                  | 模板位置                     | 说明         |
  | ------------ | ------------------------- | ---------------------------- | ------------ |
  | /user/login  | def login_view(request):  | templates/user/login.html    | 用户登陆     |
  | /user/reg    | def reg_view(request):    | templates/user/register.html | 用户注册     |
  | /user/logout | def logout_view(request): | 无                           | 退出用户登陆 |

  - 参考界面:
    - 登陆界面
      - ![](/home/tarena/1907/base04/django/day06-note/cloud_note_images/login.png)
    - 注册界面
      - ![](/home/tarena/1907/base04/django/day06-note/cloud_note_images/reg.png)

- 主页设计规范(在index应用中写代码)

  | 路由正则 | 视图函数                 | 模板位置                   | 说明 |
  | -------- | ------------------------ | -------------------------- | ---- |
  | /        | def index_view(request): | templates/index/index.html | 主页 |

  - 参考界面
    - 登陆前
      - ![](/home/tarena/1907/base04/django/day06-note/cloud_note_images/index1.png)
    - 登陆后
      - ![](/home/tarena/1907/base04/django/day06-note/cloud_note_images/index3.png)

- 云笔记设计规范

  | 路由正则        | 视图函数                    | 模板位置                      | 说明             |
  | --------------- | --------------------------- | ----------------------------- | ---------------- |
  | /note/          | def list_view(request):     | templates/note/list_note.html | 显示笔记列表功能 |
  | /note/add       | def add_view(request):      | templates/note/add_note.html  | 添加云笔记       |
  | /note/mod/(\d+) | def mod_view(request, id):  | templates/note/mod_note.html  | 修改之前云笔记   |
  | /note/del/(\d+) | def del_view(request, id):  | 无(返回列表页)                | 删除云笔记       |
  | /note/(\d+)     | def show_view(request, id): | templates/note/note.html      | 查看单个云笔记   |

  - 参考界面
    - 登陆界面
      - ![](/home/tarena/1907/base04/django/day06-note/cloud_note_images/login.png)
    - 注册界面
      - ![](/home/tarena/1907/base04/django/day06-note/cloud_note_images/reg.png)
    - 添加新笔记界面
      - ![](/home/tarena/1907/base04/django/day06-note/cloud_note_images/new_note.png)
    - 显示笔记列表
      - ![](/home/tarena/1907/base04/django/day06-note/cloud_note_images/list_note.png)
    - 修改云笔记
      - ![](/home/tarena/1907/base04/django/day06-note/cloud_note_images/mod_note.png)
    - 主页
      - 登陆前
        - ![](/home/tarena/1907/base04/django/day06-note/cloud_note_images/index1.png)
      - 登陆后
        - ![](/home/tarena/1907/base04/django/day06-note/cloud_note_images/index2.png)



## 缓存

### 什么是缓存？

缓存是一类可以更快的读取数据的介质统称，也指其它可以加快数据读取的存储方式。一般用来存储临时数据，常用介质的是读取速度很快的内存

### 为什么使用缓存？

视图渲染有一定成本，对于低频变动的页面可以考虑使用缓存技术，减少实际渲染次数

案例分析

```python
from django.shortcuts import render

def index(request):
    # 时间复杂度极高的渲染
    book_list = Book.objects.all()  #-> 此处假设耗时2s
    return render(request, 'index.html', locals())
```

优化思想

```python
given a URL, try finding that page in the cache
if the page is in the cache:
    return the cached page
else:
    generate the page
    save the generated page in the cache (for next time)
    return the generated page
```



### 使用缓存场景：

1，博客列表页

2，电商商品详情页

3，缓存导航及页脚



### Django中设置缓存

Django中提供多种缓存方式，如需使用需要在settings.py中进行配置

1,数据库缓存

Django可以将其缓存的数据存储在您的数据库中

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
        'OPTIONS':{
            'MAX_ENTRIES': 300,
            'CULL_FREQUENCY': 2,
        }
    }
}
```

创建缓存表

```python
python3 manage.py createcachetable
```



2,文件系统缓存

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',#这个是文件夹的路径
        #'LOCATION': 'c:\test\cache',#windows下示例
    }
}
```



3, 本地内存缓存

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}
```

### Django中使用缓存

- 在视图View中使用
- 在路由URL中使用
- 在模板中使用

在视图View中使用cache

```python
from django.views.decorators.cache import cache_page

@cache_page(30)  -> 单位s
def my_view(request):
    ...
```

在路由中使用

```python
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('foo/', cache_page(60)(my_view)),
]
```

在模板中使用 导航 - 欢迎XXX

```python
{% load cache %}
{% cache 500 sidebar request.user.username %}
    .. sidebar for logged in user ..
{% endcache %}

```

### 浏览器中的缓存

![浏览器缓存](/home/tarena/1907/base04/django/day07/images/浏览器缓存.png)

浏览器缓存分类：

#### 强缓存

**不会向服务器发送请求，直接从缓存中读取资源**

1，Expires

**缓存过期时间，用来指定资源到期的时间，是服务器端的具体的时间点**

Expires=max-age + 请求时间

**Expires 是 HTTP/1 的产物，受限于本地时间，如 果修改了本地时间，可能会造成缓存失效**



2, Cache-Control 

在HTTP/1.1中，Cache-Control主要用于控制网页缓存。比如当`Cache-Control:max-age=120  `代表请求创建时间后的120秒，缓存失效



横向对比   Expires  VS Cache-Control



#### 协商缓存

**协商缓存就是强制缓存失效后，浏览器携带缓存标识向服务器发起请求，由服务器根据缓存标识决定是否使用缓存的过程

1，Last-Modified和If-Modified-Since

​	第一次访问时，服务器会返回 

  Last-Modified: Fri, 22 Jul 2016 01:47:00 GMT

​	浏览器下次请求时 携带If-Modified-Since这个header , 该值为 Last-Modified

​	服务器接收请求后，对比结果，若资源未发生改变，则返回304， 否则返回200并将新资源返回给浏览器

​	缺点：只能精确到秒，容易发生单秒内多次修改，检测不到



2，ETag和If-None-Match

​	Etag是服务器响应请求时，返回当前资源文件的一个唯一标识(由服务器生成)，只要资源有变化，Etag就会重新生成

​	流程同上



对比  Last-Modified VS  ETag  

1，精度不一样 -  Etag 高

2，性能上 - Last-Modifi 高

3，优先级 - Etag 高

#### 总结(考试必背)

1.浏览器-发出请求时【浏览器地址栏回车/摁钮/超链接-get】,浏览器优先检查是否有强缓存，

​	1.如果没有强缓存，浏览器发出HTTP请求至服务器端

​	2.有强缓存-但是缓存过期：

​		尝试协商缓存 - 【Last_Modified/Etag】

​				1.Last_Modifide

​							把上次缓存响应头中的Last_Modifide的值赋值给if-Modifide-Since请求头，发送至服务器，如果服务器端对比当前响应的Modifide和请求头中一致，则返回304且响应体为空，否则返回200且响应中携带最新数据

​				2.Etag  

​							把上次缓存响应头中的Etag的值赋值给if-None-Match请求头，剩余步骤同上




## 中间件 Middleware

- 中间件是 Django 请求/响应处理的钩子框架。它是一个轻量级的、低级的“插件”系统，用于全局改变 Django 的输入或输出。
- 每个中间件组件负责做一些特定的功能。例如，Django 包含一个中间件组件 AuthenticationMiddleware，它使用会话将用户与请求关联起来。
- 他的文档解释了中间件是如何工作的，如何激活中间件，以及如何编写自己的中间件。Django 具有一些内置的中间件，你可以直接使用。它们被记录在 built-in middleware reference 中。
- 中间件类:
  - 中间件类须继承自 `django.utils.deprecation.MiddlewareMixin`类
  - 中间件类须实现下列五个方法中的一个或多个:
    - `def process_request(self, request):` 执行路由之前被调用，在每个请求上调用，返回None或HttpResponse对象 
    - `def process_view(self, request, callback, callback_args, callback_kwargs):` 调用视图之前被调用，在每个请求上调用，返回None或HttpResponse对象
    - `def process_response(self, request, response):` 所有响应返回浏览器  被调用，在每个请求上调用，返回HttpResponse对象
    - `def process_exception(self, request, exception):` 当处理过程中抛出异常时调用，返回一个HttpResponse对象
    - `def process_template_response(self, request, response):` 在视图刚好执行完毕之后被调用，在每个请求上调用，返回实现了render方法的响应对象
  - 注： 中间件中的大多数方法在返回None时表示忽略当前操作进入下一项事件，当返回HttpResponese对象时表示此请求结束，直接返回给客户端

- 编写中间件类:

```python
# file : middleware/mymiddleware.py
from django.http import HttpResponse, Http404
from django.utils.deprecation import MiddlewareMixin

class MyMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        print("中间件方法 process_request 被调用")

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("中间件方法 process_view 被调用")

    def process_response(self, request, response):
        print("中间件方法 process_response 被调用")
        return response

    def process_exception(self, request, exception):
        print("中间件方法 process_exception 被调用")

    def process_template_response(self, request, response):
        print("中间件方法 process_template_response 被调用")
        return response

```

- 注册中间件:

```python
# file : settings.py
MIDDLEWARE = [
    ...
       ]

```

- 中间件的执行过程
  - ![](/home/tarena/1907/base04/django/day07/images/middleware.jpeg)


- 练习

  - 用中间件实现强制某个IP地址只能向/test 发送 5 次GET请求

  - 提示:

    - request.META['REMOTE_ADDR'] 可以得到远程客户端的IP地址
    - request.path_info 可以得到客户端访问的GET请求路由信息

  - 答案:

    ```python
    from django.http import HttpResponse, Http404
    from django.utils.deprecation import MiddlewareMixin
    import re
    class VisitLimit(MiddlewareMixin):
        '''此中间件限制一个IP地址对应的访问/user/login 的次数不能改过5次,超过后禁止使用'''
        visit_times = {}  # 此字典用于记录客户端IP地址有访问次数
        def process_request(self, request):
            ip_address = request.META['REMOTE_ADDR']  # 得到IP地址
            if not re.match('^/test', request.path_info):
                return
            times = self.visit_times.get(ip_address, 0)
            print("IP:", ip_address, '已经访问过', times, '次!:', request.      )
            self.visit_times[ip_address] = times + 1
            if times < 5:
                return None
    
            return HttpResponse('你已经访问过' + str(times) + '次，您被禁止了')
    
    ```


## 跨站请求伪造保护 CSRF

- 跨站请求伪造攻击

  - 某些恶意网站上包含链接、表单按钮或者JavaScript，它们会利用登录过的用户在浏览器中的认证信息试图在你的网站上完成某些操作，这就是跨站请求伪造(CSRF，即Cross-Site Request Forgey)。 

- 说明:

- CSRF中间件和模板标签提供对跨站请求伪造简单易用的防护。 

- 作用:  

  - 不让其它表单提交到此 Django 服务器

- 解决方案:

  1. 取消 csrf 验证(不推荐)

     - 删除 settings.py 中 MIDDLEWARE 中的 `django.middleware.csrf.CsrfViewMiddleware` 的中间件

  2. 通过验证 csrf_token 验证

     ```python
     需要在表单中增加一个标签 
     {% csrf_token %}
     
     ```

 

## 分页

- 分页是指在web页面有大量数据需要显示，为了阅读方便在每个页面中只显示部分数据。
- 好处:
  1. 方便阅读
  2. 减少数据提取量，减轻服务器压力。
- Django提供了Paginator类可以方便的实现分页功能 
- Paginator类位于`django.core.paginator` 模块中。

### Paginator对象

- 对象的构造方法
  - Paginator(object_list, per_page)
  - 参数
    - object_list 需要分类数据的对象列表
    - per_page 每页数据个数
  - 返回值:
    - 分页对象

- Paginator属性
  - count：需要分类数据的对象总数
  - num_pages：分页后的页面总数
  - page_range：从1开始的range对象, 用于记录当前面码数
  - per_page 每页数据的个数

- Paginator方法
  - Paginator.page(number)
    - 参数 number为页码信息(从1开始)
    - 返回当前number页对应的页信息
    - 如果提供的页码不存在，抛出InvalidPage异常

- Paginator异常exception
  - InvalidPage：当向page()传入一个无效的页码时抛出
  - PageNotAnInteger：当向page()传入一个不是整数的值时抛出
  - EmptyPage：当向page()提供一个有效值，但是那个页面上没有任何对象时抛出

### Page对象

- 创建对象
  Paginator对象的page()方法返回Page对象，不需要手动构造
- Page对象属性
  - object_list：当前页上所有数据对象的列表
  - number：当前页的序号，从1开始
  - paginator：当前page对象相关的Paginator对象
- Page对象方法
  - has_next()：如果有下一页返回True
  - has_previous()：如果有上一页返回True
  - has_other_pages()：如果有上一页或下一页返回True
  - next_page_number()：返回下一页的页码，如果下一页不存在，抛出InvalidPage异常
  - previous_page_number()：返回上一页的页码，如果上一页不存在，抛出InvalidPage异常
  - len()：返回当前页面对象的个数
- 说明:
  - Page 对象是可迭代对象,可以用 for 语句来 访问当前页面中的每个对象

- 参考文档<https://docs.djangoproject.com/en/1.11/topics/pagination/>


- 分页示例:

  - 视图函数

  ```python
  from django.core.paginator import Paginator
  def book(request):
      bks = models.Book.objects.all()
      paginator = Paginator(bks, 10)
      print('当前对象的总个数是:', paginator.count)
      print('当前对象的面码范围是:', paginator.page_range)
      print('总页数是：', paginator.    )
      print('每页最大个数:', paginator.per_page)
  
      cur_page = request.GET.get('page', 1)  # 得到默认的当前页
      page = paginator.page(cur_page)
      return render(request, 'bookstore/book.html', locals())
  
  ```

  - 模板设计

  ```html
  <html>
  <head>
      <title>分页显示</title>
  </head>
  <body>
  {% for b in page %}
      <div>{{ b.title }}</div>
  {% endfor %}
  
  {# 分页功能 #}
  {# 上一页功能 #}
  {% if page.has_previous %}
  <a href="{% url 'book' %}?page={{ page.previous_page_number }}">上一页</a>
  {% else %}
  上一页
  {% endif %}
  
  {% for p in paginator.page_range %}
      {% if p == page.number %}
          {{ p }}
      {% else %}
          <a href="{% url 'book' %}?page={{ p }}">{{ p }}</a>
      {% endif %}
  {% endfor %}
  
  {#下一页功能#}
  {% if page.has_next %}
  <a href="{% url 'book' %}?page={{ page.next_page_number }}">下一页</a>
  {% else %}
  下一页
  {% endif %}
  </body>
  </html>
  ```


## 文件上传下载

```
上传：form enctype-'muiltpart/form-data'
	 input type = 'file' name = 'myfile'
	 request.FILES['myfile']
```

```
下载csv：1.换掉响应头的Content-Type ->'text/csv'
		2.添加特殊的附件响应头 Content-Disposition:'attachment:filename="my.csv"'
```

- 文件上传必须为POST提交方式
- 表单`<form>`中文件上传时必须有带有`enctype="multipart/form-data"` 时才会包含文件内容数据。
- 表单中用`<input type="file" name="xxx">`标签上传文件
  - 名字`xxx`对应`request.FILES['xxx']` 对应的内存缓冲文件流对象。可通能过`request.FILES['xxx']` 返回的对象获取上传文件数据
  - `file=request.FILES['xxx']` file 绑定文件流对象，可以通过文件流对象的如下信息获取文件数据
    file.name 文件名
    file.file 文件的字节流数据


- 上传文件的表单书写方式

  ```html
  <!-- file: index/templates/index/upload.html -->
  <html>
  <head>
      <meta charset="utf-8">
      <title>文件上传</title>
  </head>
  <body>
      <h3>上传文件</h3>
      <form method="post" action="/upload" enctype="multipart/form-data">
          <input type="file" name="myfile"/><br>
          <input type="submit" value="上传">
      </form>
  </body>
  </html>
  ```

- 在setting.py 中设置一个变量MEDIA_ROOT 用来记录上传文件的位置

  ```python
  # file : settings.py
  ...
  MEDIA_ROOT = os.path.join(BASE_DIR, 'static/files')
  ```

- 在当前项目文件夹下创建 `static/files` 文件夹

  ```shell
  $ mkdir -p static/files
  ```

- 添加路由及对应的处理函数

  ```python
  # file urls.py
  urlpatterns = [
      url(r'^admin/', admin.site.urls),
      url(r'^upload', views.upload_view)
  ]
  ```

- 上传文件的视图处理函数

  ```python
  # file views.py
  from django.http import HttpResponse, Http404
  from django.conf import settings
  import os
  
  def upload_view(request):
      if request.method == 'GET':
          return render(request, 'index/upload.html')
      elif request.method == "POST":
          a_file = request.FILES['myfile']
          print("上传文件名是:", a_file.name)
  
          filename =os.path.join(settings.MEDIA_ROOT, a_file.name)
          with open(filename, 'wb') as f:
              data = a_file.file.read()
              f.write(data)
          return HttpResponse("接收文件:" + a_file.name + "成功")
      raise Http404
  ```

- 访问地址: <http://127.0.0.1:8000/static/upload.html>


## Django用户认证

- Django带有一个用户认证系统。 它处理用户账号、组、权限以及基于cookie的用户会话。

- 作用:

  1. 添加普通用户和超级用户
  2. 修改密码

- 文档参见

- <https://docs.djangoproject.com/en/1.11/topics/auth/>

- User模型类

- 位置: `from django.contrib.auth.models import User`

- 默认user的基本属性有：

  | 属性名       | 类型                                                         | 是否必选 |
  | ------------ | ------------------------------------------------------------ | -------- |
  | username     | 用户名                                                       | 是       |
  | password     | 密码                                                         | 是       |
  | email        | 邮箱                                                         | 可选     |
  | first_name   | 名                                                           |          |
  | last_name    | 姓                                                           |          |
  | is_superuser | 是否是管理员帐号(/admin)                                     |          |
  | is_staff     | 是否可以访问admin管理界面                                    |          |
  | is_active    | 是否是活跃用户,默认True。一般不删除用户，而是将用户的is_active设为False。 |          |
  | last_login   | 上一次的登录时间                                             |          |
  | date_joined  | 用户创建的时间                                               |          |

- 数据库表现形式

```sql
mysql> use myauth;
mysql> desc auth_user;
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| id           | int(11)      | NO   | PRI | NULL    | auto_increment |
| password     | varchar(128) | NO   |     | NULL    |                |
| last_login   | datetime(6)  | YES  |     | NULL    |                |
| is_superuser | tinyint(1)   | NO   |     | NULL    |                |
| username     | varchar(150) | NO   | UNI | NULL    |                |
| first_name   | varchar(30)  | NO   |     | NULL    |                |
| last_name    | varchar(30)  | NO   |     | NULL    |                |
| email        | varchar(254) | NO   |     | NULL    |                |
| is_staff     | tinyint(1)   | NO   |     | NULL    |                |
| is_active    | tinyint(1)   | NO   |     | NULL    |                |
| date_joined  | datetime(6)  | NO   |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+
11 rows in set (0.00 sec)
```

### auth基本模型操作:

- 创建用户

  - 创建普通用户create_user

    ```python
    from django.contrib.auth import models
    user = models.User.objects.create_user(username='用户名', password='密码', email='邮箱',...)
    ...
    user.save()
    ```

  - 创建超级用户create_superuser

    ```python
    from django.contrib.auth import models
    user = models.User.objects.create_superuser(username='用户名', password='密码', email='邮箱',...)
    ...
    user.save()
    ```

- 删除用户

  ```python
  from django.contrib.auth import models
  try:
      user = models.User.objects.get(username='用户名')
      user.is_active = False  # 记当前用户无效
      user.save()
      print("删除普通用户成功！")
  except:
      print("删除普通用户失败")
  return HttpResponseRedirect('/user/info')
  ```

- 修改密码set_password

  ```python
  from django.contrib.auth import models
  try:
      user = models.User.objects.get(username='xiaonao')
      user.set_password('654321')
      user.save()
      return HttpResponse("修改密码成功！")
  except:
      return HttpResponse("修改密码失败！")
  ```

- 检查密码是否正确check_password

  ```python
  from django.contrib.auth import models
  try:
      user = models.User.objects.get(username='xiaonao')
      if user.check_password('654321'):  # 成功返回True,失败返回False
          return HttpResponse("密码正确")
      else:
          return HttpResponse("密码错误")
  except: 
      return HttpResponse("没有此用户！")
  ```

### 哈希三大特点

定长输出【无论输入多长，输出都是定长】、雪崩【一变则巨变】、不可逆【无法反算回明文】

自行处理密码存储策略
1.当用户注册时，将用户传递过来的明文密码进行 如 md5,sha系列的哈希算法【散列】；
 pw=request.POST.get('password')
 pw += 'salt'
 import hashlib
 m5 = hashlib.md5()
 m5.update(pw.encode())
 pw_md5 = md5.hexdigest()

2.当用户登录时

用户登录时填写的密码

pw = request.POST.get('password')
pw += 'salt'
import hashlib
m5 = hashlib.md5()
m5.update(pw.encode())
pw_md5 = md5.hexdigest()

user = User.objects.get(username=username)
if user.password != pw_md5：
	return '用户名或密码错误'

## 生成CSV文件

Django可直接在视图函数中生成csv文件 并响应给浏览器

```python
import csv
from django.http import HttpResponse
from .models import Book

def make_csv_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mybook.csv"'
	all_book = Book.objects.all()
    writer = csv.writer(response)
    writer.writerow(['id', 'title'])
    for b in all_book:    
    	writer.writerow([b.id, b.title])

    return response
```

- 响应获得一个特殊的MIME类型*text / csv*。这告诉浏览器该文档是CSV文件，而不是HTML文件
- 响应会获得一个额外的`Content-Disposition`标头，其中包含CSV文件的名称。它将被浏览器用于“另存为...”对话框
- 对于CSV文件中的每一行，调用`writer.writerow`，传递一个可迭代对象，如列表或元组。



## 电子邮件发送

- 利用QQ邮箱发送电子邮件
- django.core.mail 子包封装了 电子邮件的自动发送SMT协议
- 前其准备:
  1. 申请QQ号
  2. 用QQ号登陆QQ邮箱并修改设置
     - 用申请到的QQ号和密码登陆到 <https://mail.qq.com/>
     - 修改 `QQ邮箱->设置->帐户->“POP3/IMAP......服务”`
     - 校验码：ysvkdcmsmkdybcij
  3. 设置Django服务器端的，用简单邮件传输协议SMTP(Simple Mail Transfer Protocol) 发送电子邮件
- settings.py 设置

```python
# 发送邮件设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # 固定写法
EMAIL_HOST = 'smtp.qq.com' # 腾讯QQ邮箱 SMTP 服务器地址
EMAIL_PORT = 25  # SMTP服务的端口号
EMAIL_HOST_USER = 'xxxx@qq.com'  # 发送邮件的QQ邮箱
EMAIL_HOST_PASSWORD = 'ysvkdcmsmkdybcij'  # 在QQ邮箱->设置->帐户->“POP3/IMAP......服务” 里得到的在第三方登录QQ邮箱授权码
EMAIL_USE_TLS = True  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)默认false
```

视图函数中

```python
from django.core import mail
mail.send_mail(
            subject='测试',  #题目
            message='哈哈哈哈',  # 消息内容
            from_email='765512581@qq.com',  # 发送者[当前配置邮箱]
            recipient_list=['licuicui159@126.com','licui@163.com']  # 接收者邮件列表
            )
```

```
from django.core import mail
mail.send_mail(subject='测试',message='哈哈哈哈',from_email='765512581@qq.com',recipient_list=['licuicui159@126.com','licu@163.com']])
```



## 项目部署

- 项目部署是指在软件开发完毕后，将开发机器上运行的开发板软件实际安装到服务器上进行长期运行
- 部署要分以下几个步骤进行
  1. 在安装机器上安装和配置同版本的数据库
  1. django 项目迁移(在安装机器上配置与开发环境相同的python版本及依懒的包)
  1. 用 uwsgi 替代`python3 manage.py runserver` 方法启动服务器
  1. 配置 nginx 反向代理服务器
  1. 用nginx 配置静态文件路径,解决静态路径问题

1. 安装同版本的数据库

   - 安装步骤略

2. django 项目迁移

   1. 安装python

      - `$ sudo apt install python3`

   2. 安装相同版本的包

      - 导出当前模块数据包的信息:
        - `$ pip3 freeze > package_list.txt`
      - 导入到另一台新主机
        - `$ pip3 install -r package_list.txt`

   3. 将当前项目源代码复制到远程主机上(scp 命令)

      - $ sudo scp -a 当前项目源代码 远程主机地址和文件夹

      - ```
        sudo scp -a /home/tarena/django/mysite1 .zip 用户名
        @88.77.66.55:/home/root/xxx
        请输入root密码：（输入公有云对应用户、密码）
        
        ```

​        

​         4.连接公有云  

​					

    window
    xshell 安装 ssh 协议
    
    linux
    终端里 ssh 用户名@公网地址


​        


### WSGI Django工作环境部署

- WSGI (Web Server Gateway Interface)Web服务器网关接口，是Python应用程序或框架和Web服务器之间的一种接口，被广泛使用
- 它实现了WSGI协议、http等协议。Nginx中HttpUwsgiModule的作用是与uWSGI服务器进行交换。WSGI是一种Web服务器网关接口。

### uWSGI 网关接口配置 (ubuntu 18.04 配置)

- 使用 `python manage.py runserver` 通常只在开发和测试环境中使用。

- 当开发结束后，完善的项目代码需要在一个高效稳定的环境中运行，这时可以使用uWSGI

- uWSGI是WSGI的一种,它可以让Django、Flask等开发的web站点运行其中.

- 安装uWSGI

  - 在线安装 uwsgi

    ```shell
    $ sudo pip3 install uwsgi
    
    ```

  - 离线安装

    1. 在线下载安装包: 

       ```shell
       $ pip3 download uwsgi
       
       ```

       - 下载后的文件为 `uwsgi-2.0.18.tar.gz`

    2. 离线安装

       ```shell
       $ tar -xzvf uwsgi-2.0.18.tar.gz
       $ cd uwsgi-2.0.18
       $ sudo python3 setup.py install
       ```
    
       3.查看安装版本
    
    ```
    tarena@tarena:~$ uwsgi --version
    2.0.18
    ```
    
    

- 配置uWSGI

  - 添加配置文件 `项目文件夹/uwsgi.ini`

    - 如: mysite1/uwsgi.ini

    ```ini
    [uwsgi]
    # 套接字方式的 IP地址:端口号
    # socket=127.0.0.1:8000
    # Http通信方式的 IP地址:端口号
    http=127.0.0.1:8000
    # 项目当前工作目录
    chdir=/home/tarena/.../my_project 这里需要换为项目文件夹的绝对路径
    # 项目中wsgi.py文件的目录，相对于当前工作目录
    wsgi-file=my_project/wsgi.py
    # 进程个数
    process=4
    # 每个进程的线程个数
    threads=2
    # 服务的pid记录文件
    pidfile=uwsgi.pid
    # 服务的日志文件位置
    daemonize=uwsgi.log
    master=true
    ```

  - 修改settings.py  26行 

    将 DEBUG=True 改为DEBUG=False

  - 修改settings.py  28行

    将　ALLOWED_HOSTS = [] 改为　ALLOWED_HOSTS = ['*']

### uWSGI的运行管理

  ```
  创建配置文件,修改路径
  $ touch uwsgi.ini
  
  启动uwsgi
  $ ls
  db.sqlite3  index  manage.py  middleware  mysite8  static  uwsgi.ini
  
  $ sudo uwsgi --ini uwsgi.ini
  [sudo] tarena 的密码： 
  [uWSGI] getting INI configuration from uwsgi.ini
  
  $ ps aux|grep 'uwsgi'
  
  浏览器打开：http://127.0.0.1:8000/index/book
  
  终端打开日志：
  sudo vim uwsgi.log
  
  关闭uwsgi
  sudo uwsgi --stop uwsgi.pid
  
  查看uwsgi状态是否关闭
  ps aux|grep 'uwsgi'
  ```

  

  - 启动 uwsgi

    ```shell
    $ cd 项目文件夹
    $ sudo uwsgi --ini 项目文件夹/uwsgi.ini
    
    ```

  - 停止 uwsgi

    ```shell
    $ cd 项目文件夹
    $ sudo uwsgi --stop uwsgi.pid
    
    ```

  - 说明:

    - 当uwsgi 启动后,当前django项目的程序已变成后台守护进程,在关闭当前终端时此进程也不会停止。

- 测试:

  - 在浏览器端输入<http://127.0.0.1:8000> 进行测试
  - 注意，此时端口号为8000

### nginx 反向代理配置

- Nginx是轻量级的高性能Web服务器，提供了诸如HTTP代理和反向代理、负载均衡、缓存等一系列重要特性，在实践之中使用广泛。

- C语言编写，执行效率高

- nginx 作用

  - 负载均衡， 多台服务器轮流处理请求
  - 反向代理

- 原理:

- 客户端请求nginx,再由nginx 请求 uwsgi, 运行django下的python代码

- ubuntu 下 nginx 安装 
  $ sudo apt install nginx

  vim /etc/apt/sources.list
  更改国内源
  sudo apt-get update
  
- nginx 配置 

  - 修改nginx 的配置文件 /etc/nginx/sites-available/default

  在server节点下添加新的location项，指向uwsgi的ip与端口。
  
  server {
      ...
      location / {
          uwsgi_pass 127.0.0.1:8000;  # 重定向到127.0.0.1的8000端口
          include /etc/nginx/uwsgi_params; # 将所有的参数转到uwsgi下
      }
      ...
  }
  
- nginx服务控制

  ```shell
  $ sudo /etc/init.d/nginx start|stop|restart|status
  # 或
  $ sudo service nginx start|stop|restart|status
  
  ```

  > 通过 start,stop,restart,status 可能实现nginx服务的启动、停止、重启、查扑克状态等操作

- 修改uWSGI配置 

  - 修改`项目文件夹/uwsgi.ini`下的Http通信方式改为socket通信方式,如:

  ```ini
  [uwsgi]
  # 去掉如下
  # http=127.0.0.1:8000
  # 改为
  socket=127.0.0.1:8000
  
  ```

  - 重启uWSGI服务

  ```shell
  $ sudo uwsgi --stop uwsgi.pid
  $ sudo uwsgi --ini 项目文件夹/uwsgi.ini
  
  ```

- 测试:

  - 在浏览器端输入<http://127.0.0.1> 进行测试
  - 注意，此时端口号为80(nginx默认值)

### nginx 配置静态文件路径

uwsgi --version

- 解决静态路径问题

  ```ini
  # file : /etc/nginx/sites-available/default
  # 新添加location /static 路由配置，重定向到指定的绝对路径
  server {
      ...
      location /static {
          # root static文件夹所在的绝对路径,如:
           ; # 重定向/static请求的路径，这里改为你项目的文件夹
      }
      ...
  }
  ```

- 修改配置文件后需要重新启动 nginx 服务

### nginx执行流程

1.第一步

```
cd /etc/nginx/
ls
cd sites-enabled/
ls ->default
vim default
:set number   ->显示行号
找到52行： i#  try...404 
回到48行：location/{ 
		uwsgi_pass 127.0.0.1:8000;
        include /etc/nginx/uwsgi_params;
        }
：wq
```

2.重启另一个终端

```
ps aux |grep 'uwsgi'
sudo uwsgi --ini uwsgi.ini
sudo /etc/init.d/nginx restart
```

3.查看网页

```
127.0.0.1/index/book
响应头：
server:nginx/1.14.1(ubuntu)
```



### 404 界面

- 在模板文件夹内添加 404.html 模版，当视图触发Http404 异常时将会被显示

- 404.html 仅在发布版中(即setting.py 中的 DEBUG=False时) 才起作用

- 当向应处理函数触发Http404异常时就会跳转到404界面

  ```python
  from django.http import Http404
  def xxx_view(request):
      raise Http404  # 直接返回404
  ```



```sh
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```