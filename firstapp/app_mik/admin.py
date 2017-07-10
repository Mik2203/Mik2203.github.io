from django.contrib import admin
from app_mik.models import Article, Comments
# Register your models here.


class ArticleInline(admin.StackedInline):
    model = Comments
    extra = 2


class ArticleAdmin(admin.ModelAdmin):
    fields = ['article_title', 'article_text','article_image']
    list_display = ['article_title', 'article_date', 'article_image', 'bit']
    list_display_links = ['article_date']
    inlines = [ArticleInline]
    list_filter = ['article_date']
    search_fields = ['article_title', 'article_text']
    class Meta():
        model = Article

admin.site.register(Article, ArticleAdmin)