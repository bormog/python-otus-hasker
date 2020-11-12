from django.conf import settings
from .models import Question, Vote


def trending(request):
    questions = Question.objects.filter(rank__gt=0).order_by('-rank', '-date_pub')[0:settings.QUESTIONS_PER_PAGE]
    ctx = {'trending': questions}
    return ctx


def user_votes(request):
    ctx = {
        'question': {},
        'answer': {}
    }
    if request.user.is_authenticated:
        votes = Vote.objects.filter(user=request.user).select_related('content_type').\
            values_list('content_type__model', 'object_id', 'vote').all()
        for (model_name, pk, vote) in votes:
            ctx[model_name][pk] = vote
    ctx = {'votes': ctx}
    return ctx
