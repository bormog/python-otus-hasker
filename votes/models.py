from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from users.models import UserProfile


class Vote(models.Model):
    VOTE_UP = 1
    VOTE_DOWN = -1
    VOTE_CHOICES = (
        (VOTE_UP, 'Vote Up'),
        (VOTE_DOWN, 'Vote Down')
    )
    user = models.ForeignKey(UserProfile, related_name='votes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)


def on_vote_change_callback(vote):
    content_type = ContentType.objects.get(pk=vote.content_type.pk)
    related_obj = content_type.get_object_for_this_type(pk=vote.object_id)
    rank = Vote.objects.filter(content_type=vote.content_type, object_id=vote.object_id). \
        aggregate(rank=Sum('vote'))['rank']
    related_obj.update_rank(rank)


@receiver(post_save, sender=Vote)
def after_like_save_callback(sender, **kwargs):
    vote_obj = kwargs['instance']
    on_vote_change_callback(vote_obj)


@receiver(post_delete, sender=Vote)
def after_like_delete_callback(sender, **kwargs):
    vote_obj = kwargs['instance']
    on_vote_change_callback(vote_obj)


class RankedVoteModel(models.Model):
    votes = GenericRelation(Vote)
    rank = models.IntegerField(blank=True, default=0)

    class Meta:
        abstract = True

    def update_rank(self, rank):
        if not self.pk:
            return
        self.rank = rank or 0
        return self.save()

    def vote(self, user, vote):
        """
        if user not voted:
            set vote (+)
        else:
            if previous_vote == +:
                delete vote (+)
            elif previous_vote == -:
                update vote (- => +)
        """
        content_type = ContentType.objects.get_by_natural_key(self._meta.app_label, self._meta.model_name)
        try:
            previous = Vote.objects.get(user=user, object_id=self.pk, content_type=content_type)
            if previous.vote == vote:
                previous.delete()
            else:
                previous.vote = vote
                previous.save()
        except Vote.DoesNotExist:
            vote_obj = Vote(user=user, object_id=self.pk, content_type=content_type, vote=vote)
            vote_obj.save()
