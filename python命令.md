# Linux命令

更新软件源
sudo apt-get update

## 软件安装命令

$ sudo apt install 文件名

查看安装是否成功

$ uwsgi --version
2.0.18

查看进程

ps aux|grep 'uwsgi'

进入root权限

$sudo su

## vim命令

### **i编辑模式**

| i    | 在当前字符前插入字符                  |
| ---- | ------------------------------------- |
| I    | 在当前行行首插入字符                  |
| a    | 在当前字符后插入字符                  |
| A    | 在当前行行末插入字符                  |
| o    | 在当前行下插入新的一行                |
| O    | 在当前行上插入新的一行                |
| r    | 替换光标所在的字符，只替换一次        |
| R    | 一直替换光标所在的字符，一直到按下ESC |

### **:命令模式**

| :w                 | 将编辑过的文本保存                                           |
| ------------------ | ------------------------------------------------------------ |
| :w!                | 若文本属性为只读时，强制保存                                 |
| :q                 | 退出vim                                                      |
| :q!                | 不管编辑或未编辑都不保存退出                                 |
| :wq                | 保存，退出                                                   |
| :e!                | 将文档还原成最原始状态                                       |
| ZZ                 | 若文档没有改动，则不储存离开，若文档改动过，则储存后离开，等同于:wq |
| :w [filename]      | 编辑后的文档另存为filename                                   |
| :r [filename]      | 在当前光标所在行的下面读入filename文档的内容                 |
| :set nu            | 在每行的行首显示行号                                         |
| :set nonu          | 取消行号                                                     |
| n1,n2 w [filename] | 将n1到n2的内容另存为filename这个文档                         |
| :! command         | 暂时离开vim运行某个linux命令，例如 :! ls /home 暂时列出/home目录下的文件，然后会提示按回车回到vim |

### 移动光标


| h或向左方向键           | 光标向左移动一个字符                                         |
| ----------------------- | ------------------------------------------------------------ |
| j或者向下方向键         | 光标向下移动一个字符                                         |
| K或者向上方向键         | 光标向上移动一个字符                                         |
| l或者向右方向键         | 光标向右移动一个字符                                         |
| Ctrl + f 或者pageUP键   | 屏幕向前移动一页                                             |
| Ctrl + b 或者pageDOWN键 | 屏幕向后移动一页                                             |
| Ctrl + d                | 屏幕向前移动半页                                             |
| Ctrl + u                | 屏幕向后移动半页                                             |
| +                       | 光标移动到非空格符的下一列                                   |
| -                       | 光标移动到非空格符的上一列                                   |
| n空格（n是数字）        | 按下数字n然后按空格，则光标向右移动n个字符，如果该行字符数小于n，则光标继续从下行开始向右移动，一直到n |
| 0（数字0）或者Shift+6   | 移动到本行行首                                               |
| Shift+4                 | 即’$’移动到本行行尾                                          |
| H                       | 光标移动到当前屏幕的最顶行                                   |
| M                       | 光标移动到当前屏幕的中央那一行                               |
| L                       | 光标移动到当前屏幕的最底行                                   |
| G                       | 光标移动到文本的最末行                                       |
| nG（n是数字）           | 移动到该文本的第n行                                          |
| gg                      | 移动带该文本的首行                                           |
| n回车（n是数字）        | 光标向下移动n行                                              |

### 查找与替换

| /word                 | 向光标之后寻找一个字符串名为word的字符串，当找到第一个word后，按”n”继续搜后一个 |
| --------------------- | ------------------------------------------------------------ |
| ?word                 | 想光标之前寻找一个字符串名为word的字符串，当找到第一个word后，按”n”继续搜前一个 |
| :n1,n2s/word1/word2/g | 在n1和n2行间查找word1这个字符串并替换为word2，你也可以把”/”换成”#” |
| :1,$s/word1/word2/g   | 从第一行到最末行，查找word1并替换成word2                     |
| :1,$s/word1/word2/gc  | 加上c的作用是，在替换前需要用户确认                          |

### 删除/复制/粘贴

| x,X            | x为向后删除一个字符，X为向前删除一个字符         |
| -------------- | ------------------------------------------------ |
| nx（n为数字）  | 向后删除n个字符                                  |
| dd             | 删除光标所在的那一行                             |
| ndd（n为数字） | 删除光标所在的向下n行                            |
| d1G            | 删除光标所在行到第一行的所有数据                 |
| dG             | 删除光标所在行到末行的所有数据                   |
| yy             | 复制光标所在的那行                               |
| nyy            | 复制从光标所在行起向下n行                        |
| p,P            | p复制的数据从光标下一行粘贴，P则从光标上一行粘贴 |
| y1G            | 复制光标所在行到第一行的所有数据                 |
| yG             | 复制光标所在行到末行的所有数据                   |
| J              | 讲光标所在行与下一行的数据结合成同一行           |
| u              | 还原过去的操作                                   |

# 创建项目-应用

## 基本命令

->cd 到目录

cd 1907/base04/django/day08-note/mysite8
->找到  manage.py

ls    

->创建项目 
django-admin startproject mysite8

ls   ->找到项目

->创建应用

python3 manage.py startapp index

->模型类迁移2步操作

python3 manage.py makemigrations ->生成迁移文件
python3 manage.py migrate ->将迁移文件中的表结构同步至数据库

-->创建admin后台管理员

python3 manage.py createsuperuser

->开启调试环境   

python3 manage.py runserver 

->查看数据库
mysql -uroot -p123456
create database mysite6 default charset utf8 collate utf8_general_ci;
show databases;
use mysite8;
show tables;

->复制项目

tarena@tarena:~/1907/base04/django/day06$ cp -fr mysite6/ ../day07/.

## 步骤

1.创建应用 mtm

python3 manage.py startapp mtm

2.python-files  :  mtm/models.py

from django.db import models

class Author(models.Model):
    '''作家模型类'''
    name = models.CharField('作家', max_length=50)
    def __str__(self):
        return self.name
class Book(models.Model):
    title = models.CharField('书名', max_length=50)
    author = models.ManyToManyField(Author)

```
    def __str__(self):
        return self.title
```

3.模型类迁移2步操作

python3 manage.py makemigrations ->生成迁移文件
python3 manage.py migrate ->将迁移文件中的表结构同步至数据库

4.python3 manage.py shell

数据库增、删、改、查操作

5.查看表
$ mysql -uroot -p
$ show databases;
$ use mysite4;
$ show tables;

## 启动前配置

### APP配置 33行

INSTALLED_APPS = [
    ...,
    'user',  # 用户信息模块
   'music',  # 收藏模块

​	'添加应用名',

]

### middleware配置 43

MIDDLEWARE = [    

'middleware.mymiddleware.MyMw',

]

### setting.py配置 46,57,106,107

1.46行 注释 # 'django.middleware.csrf.CsrfViewMiddleware',
2.57行  TEMPLATES = [{
        'DIRS':[

os.path.join(BASE_DIR, 'templates')

],        
        }] 
3.manage.py同级新建名为  templates 的 directory 用来存放 html文件  
4.106行 LANGUAGE_CODE = 

'

zh-Hans

'
5.108行 TIME_ZONE = 

'

Asia/Shanghai

' 

### 数据库配置  80行
第一步：
#files:setting.py

#### DATABASES = {

'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'mysite8',##文件名修改
    'USER':'root',
    'PASSWORD':'123456',
    'HOST':'127.0.0.1',
    'PORT':'3306'
}

}

第二步：

#### 创建数据库

mysql -uroot -p123456
create database mysite8 default charset utf8 collate utf8_general_ci;
show databases;
use mysite8;
show tables;

第三步：

#### 主文件files:__init__.py

提供pymysql引擎支持

import pymysql
pymysql.install_as_MySQLdb()

第四步：

应用files:mtm/models.py

from django.db import models
class Bookstore(models.Model):
    title = models.CharField("姓名",max_length=20)
    price = models.DecimalField("定价",max_digits=5,decimal_places=2,default=0.0)

获取字符串

```
def __str__(self):    
	return self.title
```

    #default='2019-10-01 18:15:20'
    #DateTime=models.DateTimeField()
    
    #ImageField() --用户上传头像图
    #image=models.ImageField(
    #upload_to="static/images")

第五步：

1.生成迁移文件
python3 manage.py makemigrations

2.将迁移文件中的表结构同步至数据库
python3 manage.py migrate

第六步：

进入django shell 模拟进入pymysql操作数据库

cd 1907/base04/django/day04_note/mysite4 ->cd 到目录
ls    ->找到  manage.py
python3 manage.py shell ->进入交互模式



from bookstore.models import Book,Author,BookStore

Book.objects.create(title='python3',pub='清华大学出版社',price=20.00,market_price=25.00)

Author.objects.create(name='王老师',age=18,email='wangweichao@tedu.cn')                   
BookStore.objects.create(title='人类简史',price=26.5,desc='追溯人类的根本')

mysql> select * from bookstore_bookstore;

### 启动项目

cd 1907/base04/django/day04_note/mysite4 ->cd 到目录
ls    ->找到  manage.py
python3 manage.py runserver ->开启调试环境 

******************************************

### 静态文件配置

文件最后一行

```
STATIC_URL = '/static/'
STATICFILES_DIRS = (            os.path.join(BASE_DIR, "static"),        )
# 用户上传文件，图片，视频等存储路径
MEDIA_ROOT = os.path.join(BASE_DIR,'static/files')
```

提示：页面中写静态文件url时，端口后面的路径为
：8000/static/a.jpg

html中写静态文件url

```
    img src='/static/image/a.jpg'
    {% load static %}
    {% static 'image/a.jpg' %}
```

### Django中设置缓存

1,配置settings.py最后一行加代码，将其缓存的数据存储在您的数据库中

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

### 分布式路由配置

1.主路由 mysite4/mysite4/urls.py 配置路由

```
from django.conf.urls import url, includefrom django.contrib import admin
```

urlpatterns = [
        url(r'^admin/', admin.site.urls),

http://127.0.0.1:8000/bookstore/

​        url(r'^bookstore/', include('bookstore.urls')) , #配置主路由
​    ]

2.具体应用bookstore中 手动创建一个urls.py,匹配bookstore/后面的path
​```
    #files bookstore/urls.py
    from django.conf.urls import url
    from . import views
    urlpatterns = [          
        #http://127.0.0.1:8000/bookstore/add_book
        url(r'^add_book$', views.bookstore), 
    ]

    ```
3、具体应用bookstore中，找到views.py,编写执行函数
    ```

 ``` 
    from django.http import HttpResponse
    from django.http import HttpResponse
    from django.shortcuts import render
    #files: bookstore/views.py
    # Create your views here.
    def bookstore(request):
        return HttpResponse('这是首页4')
        # return render(request, 'music/index.html')
 ```
(4、)如果render返回一个.html页面，【路径为day04_note/mysite4/bookstore/templates/bookstore/add_book.html】）
页面标签加上：action="/bookstore/add_book"
   eg: <form action="/bookstore/add_book" method="POST">

### 创建admin后台管理员

第一步：添加自己定义模型类的后台管理数据表

pyfiles：index/admin.py

```
from django.contrib import admin
# Register your models here.

from index.models import Book
admin.site.register(Book)
```

第二步：终端创建账号

python3 manage.py createsuperuser

Username: guoxiaonao

Password: weidongdong123456

第三步：后台管理登录地址：

<http://127.0.0.1:8000/admin>

### --文件混乱解决方案

    1. 删除 所有 migrations 里所有的 000?_XXXX.py (`__init__.py`除外)
    2. 删除 数据表
        - sql> drop database mywebdb;
    3. 重新创建 数据表
        - sql> create datebase mywebdb default charset...;
    4. 重新生成migrations里所有的 000?_XXXX.py
        - python3 manage.py makemigrations
    5. 重新更新数据库
        - python3 manage.py migrate

## 启动项目

cd 1907/base04/django/day04_note/mysite4 ->cd 到目录
ls    ->找到  manage.py
python3 manage.py runserver ->开启调试环境 

## shell进入交互模式

1.自定义默认字符串

    # files:bookstore.models.py 
    class Book(models.Model):
        def __str__(self):
            return '<%s>' % (self.title)
2.模拟进入pymysql操作数据库

mysql -uroot -p123456

mysql> select * from bookstore_bookstore;

3.python3 manage.py shell

In [1]: from bookstore.models import Book,Author,BookStore
## 查询实例：

1.查询Book表中price大于等于50的信息
Book.objects.filter(price__gte=50)

2.查询Author表中姓王的人的信息

Author.objects.filter(name__startswith='王')

3.查询Author表中Email中包含"wc"的人的信息
Author.objects.filter(email__in=['wc']) 

4.批量修改
eg：修改'清华大学出版社'图书的零售价均为40
update_books = Book.objects.filter(pub='清华大学出版社')
update_books.update(market_price=40)

5.删除
def delete_book(request,book_id):
    try:
        book=Book.objects.get(id=book_id)
        book.delete()
    except:
        return HttpResponse('您提交的数据有误，请刷新重试')
    return HttpResponseRedirect('/bookstore/all_book')

5.1批量删除
In [8]: delete_books = Book.objects.filter(pub='清华大学出版社')
In [9]: delete_books.delete()

## 查询所有数据

all_res=Book.objects.all()
for book in all_res:
    print(book.title)

## 取values ，字典

Book.objects.values("title", "pub")
all_values=Book.objects.values("title", "pub")
for book in all_values:
   print(book['title'])

## 取values，元组

all_list=Book.objects.values_list("title", "pub")
for book in all_list:
    print("book=", book)

## 降序排列

all_p=Book.objects.order_by("-price")
for book in all_p:
	print("书名:", book.title, '定价:', book.price)

## get

try:
except
Book.objects.get(pub='')

## filter条件查询

In [11]: all_q=Book.objects.filter(pub='清华大学出版社',title='python3')
In [12]: all_q
Out[12]: <QuerySet [<Book: Book object>]>

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

# view层函数编写

## urls请求分发

'''
urls.py 请求的分发入口
'''
from django.conf.urls import url
from django.contrib import admin
from . import views

## 加载模板

'''viwes.py
功能函数
'''
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

```
def index(request):

# 1 通过loader加载模板
t=loader.get_template('test.html')

# 2 t对象转化成 html字符串
html=t.render('字典')

# 3 将html return 至 浏览器
return HttpResponse(html)
```

    # render方案
    dic={'username': 'guoxiaonao', 'age': 18}
    return render(request, 'test.html', dic)
    return render(request,'xxx.html',locals())

### sum(range(start,stop,step,))

输入网址: http://127.0.0.1:8000/sum?start=1&stop=101&step=1

url(r'^sum?',views.sum_view),

```
def  sum_view(request):
    start=int(request.GET.get('start'))
    print('start=',start)
    step=int(request.GET.get('step'))
    print('step=',step)
    stop=int(request.GET.get('stop'))
    print('stop=',stop)

    ###### 开始计算

​    res=sum(range(start,stop,step,))
​    print('sum=',res)
​    return HttpResponse(res)
```

### GET/POST方法  

#### 请求GET -查看网页

​    if request.method=='GET/POST':
​        request.GET.get('a',默认值)
​        request.GET.getlist('a') ->相同变量名，多个不同值

```
# http://127.0.0.1:8000/page1?a=11111&a=123456&a=789&b=654
url(r'^page1$',views.page1_view),
```

    def  page1_view(request):
        if request.method=='GET':
            #http://127.0.0.1:8000/page1?a=11111
            print(request.GET.get('a')) #11111
    
            #http://127.0.0.1:8000/page1?a=11111
            print(request.GET.getlist('a')) #['11111', '123456', '789']
    
            # http://127.0.0.1:8000/page1?a=11111&a=123456&a=789&b=654
            print(dict(request.GET))  #  {'a': ['11111', '123456', '789'], 'b': ['654']}
            html='<h1>这是编号为1的网页</h1>'
            return HttpResponse(post_html)
#### 响应POST -提交表单或者上传文件

用于新资源的建立和/或已有资源的修改。

```
def  page2_view(request):
    if request.method=='POST':
        print('my post username is')
        print(request.POST.get('user name'))
```

#### 请求头-Content-Type

GET- 由于请求体为空 所以请求头中没有 该头

POST-一定会有该头
    1.form标签提交，使用 request.POST 取值
    2.非表单提交    使用 request.body取请求体值

### 加载 n个 页面

```
url(r'^page(\d+)', views.pagen_view),
```

def  pagen_view(request,n):
    html='<h1>==这是编号为 %s 的网页==</h1>'% n
    return HttpResponse(html)

http://127.0.0.1:8000/100/add/200 加减乘除

def  cal_view(request,x,op,y):
    x=int(x)
    y=int(y)
    if op not in ['mul','add','sub']:
        return HttpResponse('Sorry~Your canshu is wrong!!')
    # 开始计算
    res=None
    if op=='add':
        res=x+y
    elif op=='mul':
        res=x*y
    else :
        res=x-y
    return HttpResponse(res)
url(r'^(\d+)/(\w+)/(\d+)', views.cal_view),

def person_view(request,name,age):
    res="姓名"+name
    res+="年龄"+age
    return HttpResponse(res)
### 命名分组

```
# 分组 r'^page(\d+)' ->page_view(request,n)[位置传参]
# 命名分组 r'^page(?P<name>\d+)' ->page_view(request,name)[关键字传参]

# http://127.0.0.1:8000/person/xiaoming/20
url(r'^person/(?P<name>\w+)/(?P<age>\d{1,2})',views.person_view),
```

def birthday_view(request,y,m,d):
    res="生日："+y+"年"+m+"月"+d+"日"
    return HttpResponse(res)

```
# 两种生日形式

# http://127.0.0.1:8000/birthday/2019/12/27
url(r'^birthday/(?P<y>\d{4})/(?P<m>\d{1,2})/(?P<d>\d{1,2})', views.birthday_view),

# http://127.0.0.1:8000/birthday/12/27/2019
url(r'^birthday/(?P<m>\d{1,2})/(?P<d>\d{1,2})/(?P<y>\d{4})',views.birthday_view),
```

## 页面调用变量

view.py

```
def test_p(request):
    dic={}
    dic['lst']=['小红', '小明', '小兰']
    dic['dict']={'username': 'guoxiaonao','age':15}
    dic['class_obj']=Dog()
    dic['say_hi']=say_hi
    dic['number']={'age':1}
    dic['script']="<script>alert(111)</script>"
    return render(request, 'test_p.html', dic)
class Dog:
    def say(self):
        return 'hahahaha'
def say_hi():
    return 'say hi'
```

test_p.html

​	调用{{变量名}} {{username}}

    lst是 {{ lst }}
    <p>lst第一个元素是 {{ lst.0 }}
    <p>lst第二个元素是 {{ lst.1 }}
    <p>lst第三个元素是 {{ lst.2 }}
    <p>dict的 用户名是 {{ dict.username }} 
    年龄是 {{ dict.age|add:2}}  --过滤器
    <p>class_obj 调用的方式是 {{class_obj.say}}</p>
    <p>say hi 直接调用 结果是 {{ say_hi}}</p>  

### if标签

```
def test_if(request):
    # /test_if?x=1
    x=int(request.GET.get('x', 0))
    dic={'x': x}
    return render(request, 'test_if.html', dic)
```

test_if.html

{% if %}业务逻辑{% endif %}

```
 {% if x > 0 %}
            <h1>{{ x }}是大于0</h1>
        {% elif x == 0 %}
            <h1>{{ x }}是等于0</h1>
        {% elif x < 0 %}
            <h1>{{ x }}是小于0</h1>
        {% endif %}
```

            <h1>{{ x }}是大于0</h1>
​        {% elif x == 0 %}
​            <h1>{{ x }}是等于0</h1>
​        {% elif x < 0 %}
​            <h1>{{ x }}是小于0</h1>
​        {% endif %}
​    '''

### form标签 计算器 
```
def cal_view(request):
    if request.method == 'GET':
        return render(request, 'cal.html')
    elif request.method == 'POST':
        # 浏览器会用form POST请求提交如下数据
        #  x=x_val & op=op_val & y=y_val
        # print(request.POST.key())
        # text框 空提交时 浏览器会带上具体text框的name及空值一并提交到服务器

x=int(request.POST.get('x',100))

x=request.POST.get('x')
if not x:

# 错误处理 将提示信息返给浏览器

​    error='Please give me x!!'
​    dic={'error': error}
​    return render(request, 'cal.html', dic)
try:
​    x=int(x)
except Exception as e:
​    print('--x is error--')
​    print(x)
​    try:
​        x=int(float(x))
​    except Exception as e:
​        error='The x is must be number!!'
​        dic={'error': error}
​        return render(request, 'cal.html', dic)

# TODO 检查y值；方法同上

op=request.POST.get('op')

y=request.POST.get('y')
if not y:

# 错误处理 将提示信息返给浏览器

​    error='Please give me y!!'
​    dic={'error': error}
​    return render(request, 'cal.html', dic)
try:
​    y=int(y)
except Exception as e:
​    print('--y is error--')
​    print(y)
​    try:
​        y=int(float(y))
​    except Exception as e:
​        error='The y is must be number!!'
​        dic={'error': error}
​        return render(request, 'cal.html', dic)
result=0
if op == 'add':
​    result=x + y
elif op == 'sub':
​    result=x - y
elif op == 'mul':
​    result=x * y
else:
​    result=x / y
return render(request, 'cal.html', locals())
```

test_cal.html

        {% if error %}
        错误提示：{{ error }}
        {% endif %}
        
        <form action='/cal' method='POST'>
                <input type='text' name="x" value="{{ x }}">
                <select name='op'>
                    <option value="add" {% if op == 'add' %}selected{% endif %}> +加 </option>
                    <option value="sub" {% if op == 'sub' %}selected{% endif %}> -减 </option>
                    <option value="mul" {% if op == 'mul' %}selected{% endif %}> *乘 </option>
                    <option value="div" {% if op == 'div' %}selected{% endif %}> /除 </option>
                </select>
                <input type='text' name="y" value={{ y }}> = <span>{{ result }}</span>
                <div>
                    <input type="submit" value='开始计算'>
                <div>
            </form>    
### for标签
```
def test_for(request):
    lst=['小红', '小兰', '小绿']
    dic={'username': '小脑', 'age': 18}
    return render(request, 'test_for.html', locals())
```

test_for.html

    {% for i in lst %}
    
    <p> {{forloop.counter}} {{ i }}</p> #正向遍历
    <p> {{forloop.revcounter}} {{ i }}</p> #反向遍历
    
    {% if forloop.first %} ===
    {% elif forloop.last %} ===
    {% endif %}
    
    {% empty %}
    <p>对不起，当前没有数据</p>
    
    {% endfor %}
### 页面继承

```
def base_view(request):
    lst=['哈哈', '嘿嘿']
    return render(request, 'base.html', locals())
def music_view(request):
    return render(request, 'music.html')
def sports_view(request):
    return render(request, 'sports.html')
```

### 过滤器

 {{ 变量|过滤器：参数名 }}

<p>
script 结果是 {{ script|safe }}
</p>

<p>
    number 结果是 {{ number.age|add:2 }}
</p>   

### 模板继承

​    1.父模板 {% block 块名 %}xxx{% endblock %}

​    2.子模板 
​        {% extends 'base.html' %}

​        子模板 重写父模板中的内容块
​        {% block block_name %}
​                    。。。--子模板块用来覆盖父模板中 block_name 块的内容

​        {% endblock block_name %} 

# django安装

## 确认当前环境

pip3 freeze|grep 'Django'
-->Django==1.11.8

如果版本号不是1.11.8，执行如下操作：
pip3 uninstall Django
pip3 install Django==1.11.8

## 笔记本

pip3 install celery
确认当前环境Django 
pip3 freeze|grep 'Django'

## celery分布式任务队列

文档：http://docs.jinkan.org/docs/celery/
检测 版本:
pip3 freeze|grep 'celery'
安装celery:
sudo pip3 install celery

## 安装成功检测版本

tarena@tarena:~$ pip3 freeze|grep 'celery'
celery==4.3.0
tarena@tarena:~$ pip3 freeze|grep 'Django'
Django==1.11.8
tarena@tarena:~$ 

## 如果版本不对

请执行 卸载+指定版本安装 ex:
卸载 -> sudo pip3 uninstall Django
指定版本安装-> sudo pip3 install Django==1.11.8

安装中途 出现红字报错， 请先翻译一下，大概率是 权限+网络不太好

# 面试必杀技

## QuerySet

print(QuerySet.query) 可查看当前orm语句具体执行的SQL语句

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