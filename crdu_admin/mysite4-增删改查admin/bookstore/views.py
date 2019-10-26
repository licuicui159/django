from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import BookStore, Book

# Create your views here.
def add_book(request):

    if request.method == 'GET':
        return render(request, 'bookstore/add_book.html')

    elif request.method == 'POST':
        #录入数据
        title = request.POST.get('title')
        if not title:
            return HttpResponse('数据有误 请退回重新填写')
        pub = request.POST.get('pub')
        price = request.POST.get('price')
        market_price = request.POST.get('m_price')
        #TODO pub price market_price 自行检查用户是否提交

        #创建数据
        Book.objects.create(title=title,pub=pub,price=price,market_price=market_price)
        return HttpResponse('添加成功')

def all_book(request):
    #获取所有书籍
    all_book = Book.objects.all()
    # l_b = []
    # for book in all_book:
    #     d = {}
    #     d['title'] = book.title
    #     d['price'] = book.price
    #     d['market_price'] = book.market_price
    #     print(d)
    #     l_b.append(d)
    #     print(l_b)
    #[{'title':'Python3', 'price':23.33},....]
    return render(request, 'bookstore/all_book.html',locals())


def detail(request, book_id):
    #书籍详情页面
    try:
        book = Book.objects.get(id=book_id)
    except Exception as e:
        return HttpResponse('您当前查阅的书籍有误')

    return render(request, 'bookstore/detail.html', locals())

def update_book(request, book_id):
    #更新书籍零售价
    #1 查
    books = Book.objects.filter(id=book_id)
    # 如果能查出数据，一定是 QuerySet集合中的第一个元素【因为id为主键，主键是唯一的】
    if not books:
        return HttpResponse('当前所查阅书籍有误')

    if request.method != 'POST':
        return HttpResponse('当前请求异常')

    market_price = request.POST.get('m_price')
    #如果books有数据，则一定为第一个元素
    book = books[0]
    # 2 赋值
    book.market_price = market_price
    # 3 存储
    book.save()
    return HttpResponseRedirect('/bookstore/all_book')


def delete_book(request, book_id):
    #删除书籍
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
    except Exception as e:
        return HttpResponse('您提交数据有误，请刷新当前页面后重试')
    return HttpResponseRedirect('/bookstore/all_book')

    























































