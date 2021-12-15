from django.db import models
from django.contrib.auth.models import User
from django.db.models import *

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _rate = models.IntegerField(default=0, db_column='rate')

    def update_rating(self):# функция сделана двумя способами, через фор и так как показано в разборе проекта
        if self.author.all():
            postRat = self.author.aggregate(postRating=Sum('rate'))
            pRat = 0
            pRat += postRat.get('postRating')
        else:
            pRat = 0
        self._rate = pRat
        comRat = 0
        for i in self.user.userCom.all():
            comRat += int(i._rate)
        self._rate = pRat * 3 + comRat
        return self._rate
        self.save()

    def __str__(self):
        return self.user


class Post(models.Model):
    CONTENT = [("NW", 'news'), ('AR', 'article')]
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=2, blank=True, choices=CONTENT, default="NW")
    create = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)
    rate = models.FloatField(default=0)
    author = models.ForeignKey(Author, related_name='author', on_delete=models.CASCADE)
    category = models.ManyToManyField('Category', through="PostCategory")

    def like(self):
        self.rate += 1
        self.save()
        return self.rate

    def dislike(self):
        if self.rate <= 0:
            self.rate = 0
            return self.rate
        else:
            return self.rate -1
        self.save()

    def preview(self):
        return f'{self.text[:123]}...'

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name="post", on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Comment(models.Model):
    text = models.TextField(blank=True)
    create = models.DateTimeField(auto_now_add=True)
    _rate = models.FloatField(default=0, db_column='rate')
    post = models.ForeignKey('Post',related_name='postCom', on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='userCom', on_delete=models.CASCADE)

    def like(self):
        self._rate += 1
        self.save()
        return self._rate

    def dislike(self):
        if self._rate <= 0:
            self._rate = 0
            return self._rate
        else:
            return self._rate -1
        self.save()
from django.db import models

# Create your models here.
