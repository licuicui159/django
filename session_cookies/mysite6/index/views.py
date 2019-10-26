from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def set_cookies(request):

    resp = HttpResponse('set is ok')
    resp.set_cookie('username', 'guoxiaonao',60*2)

    return resp

def get_cookies(request):

    username = request.COOKIES.get('username')
    if username:
        html = '欢迎 ~%s'%(username)
    else:
        html = '请登录~'
    return HttpResponse(html)

def set_session(request):

    request.session['username'] = 'guoxiaonao_s'
    return HttpResponse('set is ok')

def get_session(request):

    username = request.session.get('username')
    html = 'session 获取到 %s' %(username)
    return HttpResponse(html)

def test_cache(request):

    import time
    t1 = time.time()
    return render(request, 'index/test_cache.html', locals())

def test_csrf(request):
    if request.method == 'GET':
        return render(request, 'index/test_csrf.html')
    elif request.method == 'POST':
        return HttpResponse('提交成功')





















