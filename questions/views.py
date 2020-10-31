from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, CreateView
from django.db.models import Q

from .models import Question, Answer
from .forms import QuestionAddForm, AnswerAddForm

def handler_404(request, exception):
    return render(request, 'questions/404.html', status=404)


class QuestionList(ListView):
    paginate_by = 3
    model = Question
    template_name = 'questions/index.html'
    queryset = Question.objects.select_related('user').prefetch_related('tags')

class QuestionSearch(ListView):
    paginate_by = 3
    model = Question
    template_name = 'questions/index.html'
    queryset = Question.objects.select_related('user').prefetch_related('tags')

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.GET.get('t', None)
        if name:
            queryset = queryset.filter(tags__name=name)
        search_str = self.request.GET.get('s', None)
        if search_str:
            if 'tag:' in search_str:
                name = search_str[4:].strip()
                if name:
                    queryset = queryset.filter(tags__name=name)
            else:
                queryset = queryset.filter(Q(title__contains=search_str) | Q(content__contains=search_str))

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionAddForm
    template_name = 'questions/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuestionCreate, self).form_valid(form)


class QuestionDetail(View):
    template_name = 'questions/view.html'
    paginate_by = 20
    form_class = AnswerAddForm

    def get_question(self, pk):
        return get_object_or_404(Question.objects.select_related('user'), pk=pk)

    def paginate_answers(self, request, question):
        page = request.GET.get('page')
        answers_list = Answer.objects.filter(question=question).select_related('user')
        paginator = Paginator(answers_list, self.paginate_by)
        return paginator.get_page(page)

    def get(self, request, pk):
        question = self.get_question(pk)

        ctx = dict()
        ctx['question'] = question
        ctx['page_obj'] = self.paginate_answers(request, question)
        ctx['form'] = self.form_class()

        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        question = self.get_question(pk)

        form = self.form_class(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
            return redirect(reverse_lazy('questions:detail', kwargs={'pk': pk}))

        ctx = dict()
        ctx['question'] = question
        ctx['page_obj'] = self.paginate_answers(request, question)
        ctx['form'] = self.form_class()
        return render(request, self.template_name, ctx)
