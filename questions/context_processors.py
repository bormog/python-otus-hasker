from django.conf import settings
from django.db.models import Count
from .models import Question

def trending(request):
    questions = Question.objects_related.with_num_answers().order_by('-num_answers', '-date_pub')[0:settings.PAGINATION_LIMIT]
    ctx = {'trending': questions}
    return {}