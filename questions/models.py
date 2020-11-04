from django.db import models
from django.db.models import Count
from django.urls import reverse_lazy
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from users.models import UserProfile


# https://apirobot.me/posts/how-to-implement-liking-in-django
class Like(models.Model):
    user = models.ForeignKey(UserProfile, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'likes'

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class QuestionRelationsQuerySet(models.QuerySet):

    def with_num_answers(self):
        return self.annotate(num_answers=Count('answers'))

    def with_num_likes(self):
        return self.annotate(num_likes=Count('likes'))

    def with_tags(self):
        return self.prefetch_related('tags')

    def with_users(self):
        return self.prefetch_related('user')


class QuestionRelationsManager(models.Manager):
    def get_queryset(self):
        return QuestionRelationsQuerySet(self.model, using=self._db)

    def with_num_answers(self):
        return self.get_queryset().with_num_answers()

    def with_num_likes(self):
        return self.get_queryset().with_num_likes()

    def with_tags(self):
        return self.self.get_queryset().with_tags()

    def with_users(self):
        return self.self.get_queryset().with_users()


class Question(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(max_length=1024)
    date_pub = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag, blank=True)
    likes = GenericRelation(Like)

    objects = models.Manager()
    objects_related = QuestionRelationsManager()

    class Meta:
        ordering = ['-date_pub']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('questions:detail', args=[self.pk])

    @property
    def total_likes(self):
        return 0 #self.likes.count()

    @property
    def total_answers(self):
        return 0 #self.answers.count()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', default=None)
    content = models.TextField(max_length=1024)
    date_pub = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='answers')
    is_right = models.BooleanField(default=False, blank=True)
    likes = GenericRelation(Like)

    class Meta:
        ordering = ['-date_pub']

    def __str__(self):
        return self.content

    @property
    def total_likes(self):
        return 0 #self.likes.count()



