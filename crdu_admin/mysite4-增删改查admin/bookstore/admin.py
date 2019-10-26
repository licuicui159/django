from django.contrib import admin
from .models import *
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'market_price']
    list_display_links = ['title']
    list_filter = ['pub']
    search_fields = ['title', 'pub']
    list_editable = ['market_price']


class AuthorManager(admin.ModelAdmin):

    list_display = ['id', 'name', 'age']

admin.site.register(Book, BookAdmin)
admin.site.register(BookStore)
admin.site.register(Author, AuthorManager)

