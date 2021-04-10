from django.shortcuts import HttpResponse, render
from markdown import markdown

from .models import Article


def index(request):
    articles = Article.objects.all().only("title").order_by("-updated_time")
    return render(request, "index.html", {"articles": articles})


def detail(request, id):
    try:
        article = Article.objects.only("title", "content").get(pk=id)
    except Article.DoesNotExist:
        return HttpResponse(404)
    text = markdown(article.content, extensions=["extra"])
    return render(request, "detail.html", {"title": article.title, "text": text})
