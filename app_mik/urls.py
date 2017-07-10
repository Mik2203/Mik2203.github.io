from django.conf.urls import url
from . import views

from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    url(r'^1/', views.basic_one),
    url(r'^2/', views.template_two),
    url(r'^3/', views.template_three_simple),
    url(r'^articles/all/$', views.articles),
    url(r'^articles/get/(?P<article_id>\d+)/$', views.article),
    url(r'^articles/addlike/(?P<article_id>\d+)/$', views.addlike),
    url(r'^articles/addcomment/(?P<article_id>\d+)/$', views.addcomment),
    url(r'^articles/$', views.addcreate),
    url(r'^(?P<article_id>\d+)/get/$', views.post_update),
    # url(r'^page/(\d+)/(\d{4})$', views.articles),
    url(r'^page/(\d+)/$', views.articles),
    url(r'^$', views.articles),

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
