from django.db import models

# Create your models here.
from django.template.defaultfilters import default
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #$return "%s/%s.%s" %(instance.id, instance.id, extension)
    return "%s/%s" %(instance.id, filename)


class Article(models.Model):
    class Meta():
        db_table = 'article'
    article_title = models.CharField(max_length=500, verbose_name='Заголовок статьи')
    article_text = models.TextField(verbose_name='Описание статьи') # большое кол. символов
    article_date = models.DateTimeField(u'Дата публикиции', auto_now_add=True) # Хранить дату и время
    article_likes = models.IntegerField(default=0)
    article_image = models.ImageField(upload_to=upload_location,
                                      #upload_to="media/images/",
                                      null=True,
                                      blank=True,
                                      width_field="width_field",
                                      height_field="height_field",
                                      verbose_name=u"Изображение")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)


    def __str__(self):
        return self.article_title

    def bit(self):
        if self.article_image:
            return u'<img src="%s" width="70"/>' % self.article_image.url
        else:
            return u'(нет изображения)'

    bit.short_descriptio = u'Изображение'
    bit.allow_tags = True

    def get_absolute_url(self):
        return reverse("articles:get", kwargs={"article_id": self.id})


class Comments(models.Model):

    fields = 'comments'

    class Meta():
        db_table = 'comments'


    comments_date = models.DateTimeField(u'datetime', auto_now=True)
    comments_text = models.TextField(verbose_name = 'Комментарий')
    comments_article = models.ForeignKey(Article)
    comments_author = models.ForeignKey(User, verbose_name='Имя пользователя')


# class ImageM(models.Model):
#     fields = 'image'
#
#     class Meta():
#         db_table = 'image'
#     news_caption = models.CharField(max_length=30)
#     news_preDescription = models.CharField(max_length=100)
#     news_description = models.CharField(max_length=300)
#     news_image = models.ImageField(upload_to='media/images/')
#     news_article = models.ForeignKey(Article)

