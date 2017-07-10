from django import forms
from django.forms import ModelForm
from app_mik.models import Comments
from app_mik.models import *


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comments
        fields = ['comments_text']


# class NewForm(forms.Form):
#     class Meta():
#         model = ImageM
#         fields = ['news_image']


class PostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "article_title",
            "article_text",
            "article_image",
        ]