from django.urls import path
from .views import *

urlpatterns = [
                path('', NewsList.as_view(), name = 'allnews'),
                path('<int:pk>', News.as_view(), name="ObjNews.html"),
                path('add/', NewsCreateView.as_view(), name='add'),
                path('<int:pk>/edit', NewsUpd.as_view(), name='add'),
                path('delete/<int:pk>', NewsDel.as_view(), name='news_del'),
                ]
