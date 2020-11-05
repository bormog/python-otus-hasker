from django.conf import settings
from django.db.models import Count
from .models import Question

def trending(request):
    questions = Question.objects.filter(rank__gt=0).order_by('-rank', '-date_pub')[0:settings.QUESTIONS_PER_PAGE]
    ctx = {'trending': questions}
    return ctx