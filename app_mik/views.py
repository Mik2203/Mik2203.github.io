from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist  # проверка в БД на значание что мы ищем
from django.core.paginator import Paginator  # Список страниц <1,2,3...>
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import loader
from django.template.context_processors import csrf
from django.template.defaulttags import comment
from django.contrib.auth.models import User
from django.contrib import messages
from app_mik.forms import CommentForm, PostForm
from app_mik.models import Article, Comments


# Create your views here.

def basic_one(request):
    view = "basic_one"
    html = "<html><body>Тут наша %s вьюшка</html></body>" % view
    return HttpResponse(html)


def template_two(request):
    view = "template_two"
    t = loader.get_template('blog_0/glob_mik.html')
    html = {'name': view}
    return HttpResponse(t.render(html, request))


def template_three_simple(request):
    view = 'template_three'
    return render_to_response('blog_0/glob_mik.html', {'name': view})


def articles(request, page_number=1):
    all_articles = Article.objects.all()
    current_page = Paginator(all_articles, 2)
    # return  render_to_response('blog_0/articles.html',
    #                            {'articles': Article.objects.all(),
    #                             'username': auth.get_user(request).username}) #пользователь
    return render_to_response('blog_0/articles.html',
                              {'articles': current_page.page(page_number),
                               'username': auth.get_user(request).username})  # пользователь


# def article(request, article_id=1):
#     return render_to_response('blog_0/article.html',
#                               {'article': Article.objects.get(id=article_id),
#                                'comments': Comments.objects.filter(comments_article_id=article_id)})

def article(request, article_id=1):
    comment_form = CommentForm
    args = {}
    args.update(csrf(request))  # Защита от django, проверка форм
    args['article'] = Article.objects.get(id=article_id)
    args['comments'] = Comments.objects.filter(comments_article_id=article_id)
    args['form'] = comment_form
    args['username'] = auth.get_user(request).username  # пользователь
    return render_to_response('blog_0/article.html', args)


def addlike(request, article_id):
    try:
        if article_id in request.COOKIES:
            return_path = request.META.get('HTTP_REFERER', '/')
            return redirect(return_path)
        else:
            article = Article.objects.get(id=article_id)
            article.article_likes += 1
            article.save()
            return_path = request.META.get('HTTP_REFERER', '/')
            response = redirect(return_path)
            response.set_cookie(article_id, 'test')
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')


def addcomment(request, article_id):
    if request.POST and ('pause' not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comments_author = request.user
            comment.comments_article = Article.objects.get(id=article_id)
            form.save()
            request.session.set_expiry(60)  # 60 сек ожидания
            request.session['pause'] = True
    return redirect('/articles/get/%s/' % article_id)


# def addphoto(request, article_id):
#     formImage = NewForm(request.POST, request.FILES)
#     if formImage.is_valid():
#         photo = formImage.save(commit=False)
#         photo.news_article = Article.objects.get(id=article_id)
#         formImage.save()
#         return redirect('/')

def handle_uploaded_file(f):
    with open('/media/images/', 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)


def addcreate(request):
    form_img = PostForm(request.POST or None, request.FILES or None)
    if form_img.is_valid():
        instance = form_img.save(commit=False)
        instance.save()
        # message success
        # messages.success(request, "Successfully Created")
        # return HttpResponseRedirect(instance.get_absolute_url)
        return redirect('/')
    context = {
        "form_img": form_img,
    }
    return render(request, 'blog_0/create_photo.html', context)


def post_update(request, article_id=1):
    instance = get_object_or_404(Article, id=article_id)
    form_img = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form_img.is_valid():
        instance = form_img.save(commit=False)
        instance.save()
        # messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        # return HttpResponseRedirect(instance.get_absolute_url())


    context = {
        "article_title": instance.article_title,
        "article_text": instance.article_text,
        "article_date": instance.article_date,
        "form_img":form_img,
    }
    return render(request, "blog_0/create_photo.html", context)