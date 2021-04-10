from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=8)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    visit_count = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag, db_index=True)

    def __str__(self):
        return self.title
