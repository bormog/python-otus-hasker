from .models import Question

def trending(request):
    questions = Question.objects.order_by('-title')[0:5]
    ctx = {'trending': questions}
    return ctx