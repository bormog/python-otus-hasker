from django.apps import apps
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView

from .forms import QuestionAddForm, AnswerAddForm
from .models import Question, Answer, Vote


def handler_404(request, exception):
    return render(request, 'questions/404.html', status=404)


class QuestionList(ListView):
    paginate_by = settings.QUESTIONS_PER_PAGE
    model = Question
    template_name = 'questions/index.html'
    queryset = Question.objects_related.num_answers().tags().users()

    def get_ordering(self):
        order_by = self.request.GET.get('order_by', None)
        if order_by == 'rank':
            ordering = ('-rank', '-date_pub',)
        else:
            ordering = ('-date_pub',)
        return ordering


class QuestionSearch(ListView):
    paginate_by = settings.QUESTIONS_PER_PAGE
    model = Question
    template_name = 'questions/search.html'
    queryset = Question.objects_related.num_answers().tags().users()
    ordering = ('-rank', '-date_pub',)

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
    form_class = AnswerAddForm

    def get_question(self, pk):
        return get_object_or_404(Question.objects.select_related('user'), pk=pk)

    def paginate_answers(self, request, question):
        page = request.GET.get('page')
        answers_list = Answer.objects.filter(question=question). \
            prefetch_related('user'). \
            order_by('-rank', '-date_pub')

        paginator = Paginator(answers_list, settings.ANSWERS_PER_PAGE)
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
            self.send_email_about_new_answer(answer, question)
            return redirect(reverse_lazy('questions:detail', kwargs={'pk': pk}))

        ctx = dict()
        ctx['question'] = question
        ctx['page_obj'] = self.paginate_answers(request, question)
        ctx['form'] = self.form_class()
        return render(request, self.template_name, ctx)

    def send_email_about_new_answer(self, answer, question):
        ctx = {
            'author_username': question.user.username,
            'user_username': answer.user.username,
            'question': question,
            'question_link': self.request.build_absolute_uri(
                reverse_lazy('questions:detail', kwargs={'pk': question.pk}))
        }

        html_body = render_to_string('questions/emails/new_answer.html', ctx)
        txt_body = render_to_string('questions/emails/new_answer.txt', ctx)
        kwargs = {
            'subject': 'New answer to your question received',
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'recipient_list': [question.user.email],
            'message': txt_body,
            'html_message': html_body
        }
        # todo log this
        send_mail(**kwargs)


class QuestionAnswerAward(LoginRequiredMixin, View):

    def get(self, request, pk, answer_id):
        is_owned_by_current_user = Question.objects.filter(pk=pk, user=request.user).exists()
        if is_owned_by_current_user:
            try:
                answer = Answer.objects.get(pk=answer_id, question_id=pk)
                answer.is_right = not answer.is_right
                answer.save()
            except Answer.DoesNotExist:
                pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class VoteView(LoginRequiredMixin, View):
    redirect_field_name = None

    def get(self, request, object_name, object_id, vote):
        votes_map = {
            'up': Vote.VOTE_UP,
            'down': Vote.VOTE_DOWN
        }
        vote = votes_map.get(vote)
        if not vote:
            return HttpResponseBadRequest('Invalid vote value')
        app_label = request.resolver_match.app_name
        try:
            model_cls = apps.get_model(app_label, object_name)
            try:
                model_object = model_cls.objects.get(pk=object_id)
                model_object.vote(request.user, vote)
            except model_cls.DoesNotExist:
                return HttpResponseBadRequest('Invalid object id')
        except LookupError:
            return HttpResponseBadRequest('Invalid object name')
        if request.path != request.META.get('HTTP_REFERER'):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect('/')
