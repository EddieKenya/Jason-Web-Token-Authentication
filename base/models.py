from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status = 'published')

    options=(
        ('draft','Draft'),
        ('published','Published'),
    )

    category = models.ForeignKey(Subject, on_delete=models.CASCADE , default=1)
    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True)
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=options, default='published')
    objects = models.Manager()
    postobjects = PostObjects()
    class Meta:
        ordering = ('-published',)


    def __str__(self): 
        return self.title