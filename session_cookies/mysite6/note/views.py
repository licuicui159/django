from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from user.models import User
from .models import *

def check_logging(fn):
    def wrap(request, *args, **kwargs):
        #检查当前用户是否登录
        #检查session
        if 'username' not in request.session or 'uid' not in request.session:
            #有可能没登录
            #检查cookie
            if 'username' not in request.COOKIES or 'uid' not in request.COOKIES:
                #肯定没登录
                return HttpResponseRedirect('/user/login')
            else:
                #回写session
                request.session['username'] = request.COOKIES['username']
                request.session['uid'] = request.COOKIES['uid']

        return fn(request, *args, **kwargs)
    return wrap

# Create your views here.
@check_logging
def add_view(request):
    if request.method == 'GET':

        return render(request, 'note/add_note.html')
    elif request.method == 'POST':
        #处理数据
        #考虑登录状态
        uid = request.session.get('uid')
        if not uid:
            return HttpResponse('请先登录')
        user = User.objects.filter(id=uid)
        #TODO 检查用户是否可以发表言论
        user = user[0]
        title = request.POST.get('title')
        content = request.POST.get('content')
        #TODO 检查 title content 是否提交
        note = Note(title=title,content=content,user=user)
        note.save()
        return HttpResponseRedirect('/note/')

@cache_page(30)
@check_logging
def list_view(request):
    #返回用户所有笔记
    uid = request.session.get('uid')
    #方案1 常规sql方案
    #all_notes = Note.objects.filter(isActive=True,user_id=uid)
    #方案2 反向查询 user 一    note 多【外键】
    user = User.objects.get(id=uid)
    all_notes = user.note_set.filter(isActive=True)
    #return render(request, 'note/list_note.html')
    return render(request, 'note/list_note.html', locals())


@check_logging
def del_view(request, id):
    #删除笔记
    uid = request.session.get('uid')
    #方案1
    notes = Note.objects.filter(id=id, user_id=uid)
    #方案2
    # user = User.objects.get(id=uid)
    # note = Note.objects.filter(id=id,user=user)
    #伪删除
    note = notes[0]
    note.isActive = False
    note.save()
    return HttpResponseRedirect('/note/')


















