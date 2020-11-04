from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Count, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy

from users.models import UserProfile


class Vote(models.Model):
    VOTE_LIKE = 1
    VOTE_DISLIKE = -1
    VOTE_CHOICES = (
        (VOTE_LIKE, 'Like'),
        (VOTE_DISLIKE, 'Dislike')
    )
    user = models.ForeignKey(UserProfile, related_name='votes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Vote)
def after_like_save_callback(sender, **kwargs):
    vote_obj = kwargs['instance']
    content_type = ContentType.objects.get(pk=vote_obj.content_type.pk)
    related_obj = content_type.get_object_for_this_type(pk=vote_obj.object_id)
    rank = Vote.objects.filter(content_type=vote_obj.content_type, object_id=vote_obj.object_id). \
        aggregate(rank=Sum('vote'))['rank']
    related_obj.update_rank(rank)


class RankedVoteModel(models.Model):
    votes = GenericRelation(Vote)
    rank = models.IntegerField(blank=True, default=0)

    class Meta:
        abstract = True

    def update_rank(self, rank):
        if not self.pk:
            return
        self.rank = rank
        return self.save()

    def vote(self, user, vote):
        pass


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
