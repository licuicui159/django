# 创建项目

cd 1907/base04/django/ ->cd 到目录
django-admin startproject 项目名  ->创建项目
python3 manage.py startapp sports ->创建应用

# 启动项目

cd 1907/base04/django/day03_note/mysite3 ->cd 到目录
ls    ->找到  manage.py
python3 manage.py runserver ->开启调试环境

# 调试前 setting.py配置 

​    1.46行 注释 # 'django.middleware.csrf.CsrfViewMiddleware',
​    2.57行  TEMPLATES = [{
​            'DIRS':[os.path.join(BASE_DIR, 'templates')],        
​            }]     
​    3.106行 LANGUAGE_CODE = 'zh-Hans'
​    4.108行 TIME_ZONE = 'Asia/Shanghai' 
​    5.manage.py同级新建名为  templates 的 Python package 用来存放 html文件  
​    

# 有静态文件请求，文件最后一行加上代码   

6.STATICFILES_DIRS = (
            os.path.join(BASE_DIR, "static"),
        )

# APP安装应用配置 33行

​        INSTALLED_APPS = [
​            ...,
​            'user',  # 用户信息模块
​            'music',  # 收藏模块
​        ]		

#### 数据库配置  80行


		第一步：
		#files:setting.py
		DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'mysite3',
			'USER':'root',
			'PASSWORD':'123456',
			'HOST':'127.0.0.1',
			'PORT':'3306'
		}
	}
		
		第二步：
	    
	    # 安装pymysql 模块
	    $ sudo pip install pymysql
		$ mysql -uroot -p
		$ create database mysite3 default charset utf8 collate utf8_general_ci;
		$ show databases;
		$ use mysites3;
		$ show tables;
	    
		# files:__init__.py  提供pymysql引擎支持
		import pymysql
		pymysql.install_as_MySQLdb()
		
		# files:models.py
		# Create your models here.
		from django.db import models
		class Bookstore(models.Model):
			title = models.CharField("姓名",max_length=20)
			price = models.DecimalField("定价",max_digits=5,decimal_places=2,default=0.0)
	
	    # DateTime=models.DateTimeField()
	    default='2019-10-01 18:15:20'
	    # ImageField() --用户上传头像图
	    image=models.ImageField(
	        upload_to="static/images")

#### **每次修改完模型类都需要做以下两步迁移操作。**​	

```
	    1.生成或更新迁移文件
		python3 manage.py makemigrations
	    2.执行迁移脚本程序
		python3 manage.py migrate
```

# 数据库的迁移文件混乱的解决办法

1. 删除 所有 migrations 里所有的 000?_XXXX.py (`__init__.py`除外)
2. 删除 数据表
    - sql> drop database mywebdb;
3. 重新创建 数据表
    - sql> create datebase mywebdb default charset...;
4. 重新生成migrations里所有的 000?_XXXX.py
    - python3 manage.py makemigrations
5. 重新更新数据库
    - python3 manage.py migrate

*****************************************

五、代码编写

'''
urls.py 请求的分发入口
'''
from django.conf.urls import url
from django.contrib import admin
from . import views

'''viwes.py
功能函数
'''
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

# render/loader加载模板
```
def index(request):

# 1 通过loader加载模板
t=loader.get_template('test.html')

# 2 t对象转化成 html字符串
html=t.render()

# 3 将html return 至 浏览器
return HttpResponse(html)
```

    # render方案
    dic={'username': 'guoxiaonao', 'age': 18}
    return render(request, 'test.html', dic)

# sum(range(start,stop,step,))

输入网址: http://127.0.0.1:8000/sum?start=1&stop=101&step=1

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
url(r'^sum?',views.sum_view),
```



# GET方法  查看网页

 http://127.0.0.1:8000/page1?a=11111&a=123456&a=789&b=654

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
url(r'^page1$',views.page1_view),

# POST方法  提交表单或者上传文件

用于新资源的建立和/或已有资源的修改。

def  page2_view(request):
    if request.method=='POST':
        print('my post username is')
        print(request.POST.get('user name'))

    html='<h1>这是编号为2的网页</h1>'
    return HttpResponse(post2_html)

# 加载 n个 页面
def  pagen_view(request,n):
    html='<h1>==这是编号为 %s 的网页==</h1>'% n
    return HttpResponse(html)
url(r'^page(\d+)', views.pagen_view),

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
# 加载用户姓名

http://127.0.0.1:8000/person/xiaoming/20

url(r'^person/(?P<name>\w+)/(?P<age>\d{1,2})',views.person_view),

def birthday_view(request,y,m,d):
    res="生日："+y+"年"+m+"月"+d+"日"
    return HttpResponse(res)
# 两种生日形式

http://127.0.0.1:8000/birthday/2019/12/27

url(r'^birthday/(?P<y>\d{4})/(?P<m>\d{1,2})/(?P<d>\d{1,2})', views.birthday_view),

http://127.0.0.1:8000/birthday/12/27/2019

url(r'^birthday/(?P<m>\d{1,2})/(?P<d>\d{1,2})/(?P<y>\d{4})',views.birthday_view),

# 页面传参
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
test_p.html
    '''
    lst是 {{ lst }}
    <p>lst第一个元素是 {{ lst.0 }}
    <p>lst第二个元素是 {{ lst.1 }}
    <p>lst第三个元素是 {{ lst.2 }}
    <p>dict的 用户名是 {{ dict.username }} 年龄是 {{ dict.age|add:2}}
    <p>class_obj 调用的方式是 {{class_obj.say}}</p>
    <p>say hi 直接调用 结果是 {{ say_hi}}</p>

    <p>
        script 结果是 {{ script|safe }}
    </p>
    
    <p>
        number 结果是 {{ number.age|add:2 }}
    </p>
    '''

# if标签
def test_if(request):
    # /test_if?x=1
    x=int(request.GET.get('x', 0))
    dic={'x': x}
    return render(request, 'test_if.html', dic)
test_if.html
    '''
        {% if x > 0 %}
            <h1>{{ x }}是大于0</h1>
        {% elif x == 0 %}
            <h1>{{ x }}是等于0</h1>
        {% elif x < 0 %}
            <h1>{{ x }}是小于0</h1>
        {% endif %}
    '''

# form标签 计算器 
def cal_view(request):
    if request.method == 'GET':
        return render(request, 'cal.html')
    elif request.method == 'POST':
        # 浏览器会用form POST请求提交如下数据
        #  x=x_val & op=op_val & y=y_val
        # print(request.POST.key())

        # text框 空提交时 浏览器会带上具体text框的name及空值一并提交到服务器
        # x=int(request.POST.get('x',100))
    
        x=request.POST.get('x')
        if not x:
            # 错误处理 将提示信息返给浏览器
            error='Please give me x!!'
            dic={'error': error}
            return render(request, 'cal.html', dic)
        try:
            x=int(x)
        except Exception as e:
            print('--x is error--')
            print(x)
            try:
                x=int(float(x))
            except Exception as e:
                error='The x is must be number!!'
                dic={'error': error}
                return render(request, 'cal.html', dic)
    
        # TODO 检查y值；方法同上
    
        op=request.POST.get('op')
    
        y=request.POST.get('y')
        if not y:
            # 错误处理 将提示信息返给浏览器
            error='Please give me y!!'
            dic={'error': error}
            return render(request, 'cal.html', dic)
        try:
            y=int(y)
        except Exception as e:
            print('--y is error--')
            print(y)
            try:
                y=int(float(y))
            except Exception as e:
                error='The y is must be number!!'
                dic={'error': error}
                return render(request, 'cal.html', dic)
        result=0
        if op == 'add':
            result=x + y
        elif op == 'sub':
            result=x - y
        elif op == 'mul':
            result=x * y
        else:
            result=x / y
        return render(request, 'cal.html', locals())
test_cal.html
    '''
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
            '''
    
# for标签
def test_for(request):
    lst=['小红', '小兰', '小绿']
    dic={'username': '小脑', 'age': 18}
    return render(request, 'test_for.html', locals())
test_for.html
    '''
        {% for i in lst %}
        <!--<p> {{forloop.counter}} {{ i }}</p> #正向遍历-->
        <p> {{forloop.revcounter}} {{ i }}</p> --反向遍历
        {% if forloop.first %} ===
        {% elif forloop.last %} %%%
        {% endif %}
        <br>

        {% empty %}
        <p>对不起，当前没有数据</p>
        {% endfor %}
    '''

# 页面继承
def base_view(request):
    lst=['哈哈', '嘿嘿']
    return render(request, 'base.html', locals())
def music_view(request):
    return render(request, 'music.html')
def sports_view(request):
    return render(request, 'sports.html')

2.项目名-文件夹->setting.py urls.py wsgi.py  
3.url.py->
    urlpatterns=[
        #url http://127.0.0.1:8000/sum?start=1&stop=101&step=1
        url(r'xxxxxx',viewes),
    ]  
    * 分组 
        r'^page(\d+)' ->page_view(request,n)[位置传参]
    *命名分组
        r'^page(?P<name>\d+)' ->page_view(request,name)[关键字传参]
4.视图函数 -> 项目同名目录下创建views.py ->
    def xxx_view(request,xx):
        try:
            a=1
        except Excetiom as e :
            print(e)
        return HttpResponse/HttpResponseRedirect
    
     响应头
        Content-Type - text/html;charset=utf-8
        Location -302    
5.请求GET 与 响应POST
    if request.method=='GET/POST':
        request.GET.get('a',默认值)
        request.GET.getlist('a') ->相同变量名，多个不同值
    请求头-Content-Type
        .GET- 由于请求体为空 所以请求头中没有 该头
        .POST-一定会有该头
            1.form标签提交，使用 request.POST 取值
            2.非表单提交    使用 request.body取请求体值
6.设计模式 MVC+MTV
7.模板： 
    第一步：配置setting.py  DIRS=[os.path.join(BASE_DIR,'templates')]  #当前项目HTML存储位置
    第二步：view层调用
        1.t=loader.get_template('模板文件名'）
            html=t.render('字典')
            return HttpResponse(html)
        2.from django.shortcuts import render
               dic={'username':'guoxiaonao'}
               return render(request,'xxx.html',dic)
               return render(request,'xxx.html',locals())
        3.调用{{变量名}} {{username}}
        4.{% 标签 %} - 流程控制 if for
            {% if %}业务逻辑{% endif %}
        5.过滤器 {{ 变量|过滤器：参数名 }}
        6.模板继承
            父模板 {% block 块名 %}xxx{% endblock %}
            子模板 
                {% extends 'base.html' %}
                子模板 重写父模板中的内容块
                {% block block_name %}
                子模板块用来覆盖父模板中 block_name 块的内容
                {% endblock block_name %}                 
