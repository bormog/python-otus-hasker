from django.test import TestCase

from questions.models import Question
from votes.models import Vote
from .fixtures import QuestionFactory, AnswerFactory


class TestQuestion(TestCase):

    def test_question_has_date_pub(self):
        question = QuestionFactory.create()
        self.assertIsNotNone(question.date_pub)


class TestAnswer(TestCase):

    def test_answer_has_date_pub(self):
        answer = AnswerFactory.create()
        self.assertIsNotNone(answer.date_pub)


class TestQuestionVotes(TestCase):

    def setUp(self):
        self.question = QuestionFactory()
        self.user = self.question.user

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
