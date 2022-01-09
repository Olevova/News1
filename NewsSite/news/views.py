from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import *
from django.views.generic import ListView, DetailView,CreateView,DeleteView, UpdateView
from .filters import PostFilter
from .form import NewsForm
from django.contrib.auth.models import Group


class NewsList(ListView):#вывод списка новостей
    model = Post
    template_name = "news.html"
    context_object_name = 'news'
    queryset = Post.objects.order_by('-create')#сортировка новостей по добавлению
    paginate_by = 4 # пагинация с выводом 4 новостей

    def get_filter(self):
        #print(super().get_queryset())
        return PostFilter(self.request.GET,queryset=super().get_queryset())

    def get_queryset(self):
        #print(self.get_filter().qs)
        return self.get_filter().qs


    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs),
                'filter': self.get_filter,
                }

class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_Post')
    template_name = 'news_create.html'
    form_class = NewsForm
    success_url = '/'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        print(context)
        return context

class News(DetailView):#вывод для одной новости
    model = Post
    template_name = 'ObjNews.html'
    context_object_name = 'piece'
    queryset = Post.objects.all()

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timenow'] = datetime.now()
        context['auf'] = Author.objects.all()
        return context

class NewsDel( LoginRequiredMixin , DeleteView):
    login_url = '/'
    template_name = 'news_del.html'
    context_object_name = "piece"
    queryset = Post.objects.all()
    success_url = '/news/'

class NewsUpd(LoginRequiredMixin,UpdateView):
    login_url = '/'
    template_name = 'news_create.html'
    form_class = NewsForm

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        print(context)
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')
