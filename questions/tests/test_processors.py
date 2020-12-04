import random

from django.conf import settings
from django.shortcuts import reverse
from django.test import TestCase

from .fixtures import QuestionFactory


class TestContextProcessor(TestCase):

    def test_trending_question_available_in_context(self):
        response = self.client.get(reverse('questions:index'))
        self.assertIn('trending', response.context)

    def test_trending_question_is_sorted_by_rank(self):
        ranks = list(range(1, settings.QUESTIONS_PER_PAGE))
        random.shuffle(ranks)

        for rank in ranks:
            QuestionFactory.create(rank=rank)

        response = self.client.get(reverse('questions:index'))
        trending = response.context['trending']
        trending_ranks = [question.rank for question in trending]
        self.assertEqual(sorted(ranks, reverse=True), trending_ranks)

    def test_user_votes_available_in_context(self):
        response = self.client.get(reverse('questions:index'))
        self.assertIn('votes', response.context)
        self.assertIn('question', response.context['votes'])
        self.assertIn('answer', response.context['votes'])
