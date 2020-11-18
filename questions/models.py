from django.db import models
from django.db.models import Count
from django.urls import reverse_lazy

from users.models import UserProfile
from votes.models import RankedVoteModel


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class QuestionRelationsQuerySet(models.QuerySet):

    def num_answers(self):
        return self.annotate(num_answers=Count('answers', distinct=True))

    def tags(self):
        return self.prefetch_related('tags')

    def users(self):
        return self.prefetch_related('user')


class QuestionRelationsManager(models.Manager):
    def get_queryset(self):
        return QuestionRelationsQuerySet(self.model, using=self._db)

    def num_answers(self):
        return self.get_queryset().num_answers()

    def tags(self):
        return self.self.get_queryset().tags()

    def users(self):
        return self.self.get_queryset().users()

    def trending(self, limit):
        return self.get_queryset().filter(rank__gt=0).order_by('-rank', '-date_pub')[0:limit]


class Question(RankedVoteModel):
    title = models.CharField(max_length=256)
    content = models.TextField(max_length=1024)
    date_pub = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag, blank=True)

    objects = models.Manager()
    objects_related = QuestionRelationsManager()

    class Meta:
        ordering = ['-date_pub']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('questions:detail', args=[self.pk])


class Answer(RankedVoteModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', default=None)
    content = models.TextField(max_length=1024)
    date_pub = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='answers')
    is_right = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ['-date_pub']

    def __str__(self):
        return self.content
