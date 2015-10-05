from django.conf.urls import patterns, url

from miniblog import views

urlpatterns = patterns('',
    url(r'^blog/$', views.article_list , name='articlelist'), 
    url(r'^article/(?P<article_id>\d+)/$', views.article_show, name='detail'), 
    url(r'^article/tag/(?P<tag_id>\d+)/$', views.article_filter, name='articlefilter'),
    url(r'^article/add/$', views.article_add, name='addarticle'),
    url(r'^article/(?P<article_id>\w+)/update/$', views.article_update, name='updarticle'),
    url(r'^aritcle/(?P<article_id>\w+)/del/$', views.article_delete, name='delarticle'),
    url(r'^blog_note/$', views.blog_note , name='blog_note'), 
    url(r'^blog_note/(?P<article_id>\d+)/$', views.blog_note_show , name='blog_note_show'), 
)