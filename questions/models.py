from django.db import models, transaction, IntegrityError
from django.db.models import Count, Sum
from django.urls import reverse_lazy
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from users.models import UserProfile


class Like(models.Model):
    VOTE_LIKE = 1
    VOTE_DISLIKE = -1
    VOTE_CHOICES = (
        (VOTE_LIKE, 'Like'),
        (VOTE_DISLIKE, 'Dislike')
    )
    user = models.ForeignKey(UserProfile, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        db_table = 'likes'

    def save(self, *args, **kwargs):
        # todo transaction, check if exists method and callable
        # todo https://docs.djangoproject.com/en/3.1/ref/signals/#django.db.models.signals.post_save
        super().save(*args, **kwargs)
        result = Like.objects.filter(content_type=self.content_type, object_id=self.object_id).\
                    aggregate(Sum('vote'))
        content_type = ContentType.objects.get(pk=self.content_type.pk)
        related_obj = content_type.get_object_for_this_type(pk=self.object_id)
        related_obj.update_rank(result['vote__sum'])

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class RankedModel(models.Model):
    likes = GenericRelation(Like)
    rank = models.IntegerField(blank=True, default=0)

    class Meta:
        abstract = True

    def update_rank(self, rank):
        self.rank = rank
        return self.save()



class QuestionRelationsQuerySet(models.QuerySet):

    def with_num_answers(self):
        return self.annotate(num_answers=Count('answers', distinct=True))

    def with_tags(self):
        return self.prefetch_related('tags')

    def with_users(self):
        return self.prefetch_related('user')


class QuestionRelationsManager(models.Manager):
    def get_queryset(self):
        return QuestionRelationsQuerySet(self.model, using=self._db)

    def with_num_answers(self):
        return self.get_queryset().with_num_answers()

    def with_tags(self):
        return self.self.get_queryset().with_tags()

    def with_users(self):
        return self.self.get_queryset().with_users()


class Question(RankedModel):
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


class Answer(RankedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', default=None)
    content = models.TextField(max_length=1024)
    date_pub = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='answers')
    is_right = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ['-date_pub']

    def __str__(self):
        return self.content



