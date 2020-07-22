"""my_blog/blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import IndexView, DetailView, ArticleCreateView, test
# from .views import (IndexView, DetailView)#, DetailView, CategoryView, TagView, AboutView,
                    #SilianView, MySearchView, ArchiveView, TimelineView)

app_name = 'blog'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blog/', IndexView.as_view(), name='index'),
    path('article/<slug:slug>/', DetailView.as_view(), name='detail'),  # 文章内容页
    path('article-create/', ArticleCreateView.as_view(), name='article_create'), #新建文章
    path('test/',test,name='test'),
]
