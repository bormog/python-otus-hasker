from .models import Question

def trending(request):
    questions = Question.objects.order_by('-title')[0:20]
    ctx = {'trending': questions}
    return ctx