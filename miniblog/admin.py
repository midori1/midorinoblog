from django.contrib import admin
from miniblog.models import Author, Article, Tag, Classification, RootClassification
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    """docstring for AuthorAdmin"""
    list_display = ('name', 'email', 'website')
    search_fields = ('name',)
class ArticleAdmin(admin.ModelAdmin):
    """docstring for ArticleAdmin"""
    list_display = ('caption', 'id', 'author', 'publish_time')
    list_filter = ('publish_time',)
    date_hierarchy = 'publish_time'
    ordering = ('-publish_time',)
    filter_horizontal = ('tags',)
    # raw_id_fields = ('author',)  
admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Classification)
admin.site.register(RootClassification)