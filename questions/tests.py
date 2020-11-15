import random
from django.conf import settings
from django.test import TestCase

from votes.models import Vote
from users.models import UserProfile
from .models import Question, Answer


class TestQuestion(TestCase):

    def test_question_has_date_pub(self):
        user = UserProfile.objects.create_user('foobar', 'foobar@foobar.com', 'foobar')
        question = Question.objects.create(title='foobar', content='foobar', user=user)
        self.assertIsNotNone(question.date_pub)


class TestAnswer(TestCase):

    def test_question_has_date_pub(self):
        user = UserProfile.objects.create_user('foobar', 'foobar@foobar.com', 'foobar')
        question = Question.objects.create(title='foobar', content='foobar', user=user)
        answer = Answer.objects.create(content='foobar', question=question, user=user)
        self.assertIsNotNone(answer.date_pub)


class TestQuestionVotes(TestCase):

    def setUp(self):
        self.user = UserProfile.objects.create_user('foobar', 'foobar@foobar.com', 'foobar')
        self.question = Question.objects.create(title='foobar', content='foobar', user=self.user)

    def test_question_rank_up(self):
        self.assertEqual(0, self.question.rank)
        self.question.vote(self.user, Vote.VOTE_UP)
        question = Question.objects.get(pk=self.question.pk)
        self.assertEqual(question.rank, Vote.VOTE_UP)

    def test_question_rank_down(self):
        self.assertEqual(0, self.question.rank)
        self.question.vote(self.user, Vote.VOTE_DOWN)
        question = Question.objects.get(pk=self.question.pk)
        self.assertEqual(question.rank, Vote.VOTE_DOWN)

    def test_question_vote_up_cancelled(self):
        self.assertEqual(0, self.question.rank)
        self.question.vote(self.user, Vote.VOTE_UP)
        self.question.vote(self.user, Vote.VOTE_UP)
        question = Question.objects.get(pk=self.question.pk)
        self.assertEqual(question.rank, 0)

    def test_question_vote_down_cancelled(self):
        self.assertEqual(0, self.question.rank)
        self.question.vote(self.user, Vote.VOTE_DOWN)
        self.question.vote(self.user, Vote.VOTE_DOWN)
        question = Question.objects.get(pk=self.question.pk)
        self.assertEqual(question.rank, 0)

    def test_question_vote_changed_from_up_to_down(self):
        self.assertEqual(0, self.question.rank)
        self.question.vote(self.user, Vote.VOTE_UP)
        self.question.vote(self.user, Vote.VOTE_DOWN)
        question = Question.objects.get(pk=self.question.pk)
        self.assertEqual(question.rank, Vote.VOTE_DOWN)

    def test_question_vote_changed_from_down_to_up(self):
        self.assertEqual(0, self.question.rank)
        self.question.vote(self.user, Vote.VOTE_DOWN)
        self.question.vote(self.user, Vote.VOTE_UP)
        question = Question.objects.get(pk=self.question.pk)
        self.assertEqual(question.rank, Vote.VOTE_UP)


class TestContextProcessor(TestCase):

    def test_trending_question_available_in_context(self):
        response = self.client.get('/')
        self.assertIn('trending', response.context)

    def test_trending_question_is_sorted_by_rank(self):
        ranks = list(range(1, settings.QUESTIONS_PER_PAGE))
        random.shuffle(ranks)

        user = UserProfile.objects.create_user('foobar', 'foobar@foobar.com', 'foobar')
        for rank in ranks:
            Question.objects.create(title='foobar', content='foobar', user=user, rank=rank)

        response = self.client.get('/')
        trending = response.context['trending']
        trending_ranks = [question.rank for question in trending]
        self.assertEqual(sorted(ranks, reverse=True), trending_ranks)

    def test_user_votes_available_in_context(self):
        response = self.client.get('/')
        self.assertIn('votes', response.context)
        self.assertIn('question', response.context['votes'])
        self.assertIn('answer', response.context['votes'])

