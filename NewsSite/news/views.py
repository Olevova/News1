from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView


class NewsList(ListView):#вывод списка новостей
    model = Post
    template_name = "news.html"
    context_object_name = 'news'
    queryset = Post.objects.order_by('-create')#сортировка новостей по добавлению



class News(DetailView):#вывод для одной новости
    model = Post
    template_name = 'ObjNews.html'
    context_object_name = 'piece'

from django.shortcuts import render

# Create your views here.
