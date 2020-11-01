from .models import Question
from django.db.models import Count

def trending(request):
    questions = Question.objects.annotate(num_answers=Count('answers')).order_by('-num_answers', '-date_pub')[0:20]
    ctx = {'trending': questions}
    return ctx