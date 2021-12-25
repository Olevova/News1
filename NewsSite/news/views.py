from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.generic import ListView, DetailView,CreateView,DeleteView, UpdateView
from .filters import PostFilter
from .form import NewsForm


class NewsList(ListView):#вывод списка новостей
    model = Post
    template_name = "news.html"
    context_object_name = 'news'
    queryset = Post.objects.order_by('-create')#сортировка новостей по добавлению
    paginate_by = 4 # пагинация с выводом 4 новостей

    def get_filter(self):
        #print(super().get_queryset())
        return PostFilter(self.request.GET,queryset =super().get_queryset())

    def get_queryset(self):
        #print(self.get_filter().qs)
        return self.get_filter().qs


    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs),
                'filter': self.get_filter,
                }

class NewsCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = NewsForm

class News(DetailView):#вывод для одной новости
    model = Post
    template_name = 'ObjNews.html'
    context_object_name = 'piece'
    queryset = Post.objects.all()

class NewsDel(DeleteView):
    template_name = 'news_del.html'
    context_object_name = "piece"
    queryset = Post.objects.all()
    success_url = '/news/'

class NewsUpd(UpdateView):
    template_name = 'news_create.html'
    form_class = NewsForm

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)



