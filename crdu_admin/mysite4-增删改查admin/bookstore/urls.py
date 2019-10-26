from django.conf.urls import url
from . import views
#file mysite4/bookstore/urls.py
urlpatterns = [
    #http://127.0.0.1:8000/bookstore/add_book
    url(r'^add_book', views.add_book),
    #http://127.0.0.1:8000/bookstore/all_book
    url(r'^all_book', views.all_book),
    #http://127.0.0.1:8000/bookstore/detail/3
    url(r'^detail/(\d+)', views.detail),
    #http://127.0.0.1:8000/bookstore/update_book/3
    url(r'^update_book/(\d+)', views.update_book),
    #http://127.0.0.1:8000/bookstore/delete_book/3
    url(r'^delete_book/(\d+)', views.delete_book)
]