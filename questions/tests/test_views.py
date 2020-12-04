from django.conf import settings
from django.shortcuts import reverse
from django.test import TestCase

from .fixtures import QuestionFactory, AnswerFactory


class TestQuestionView(TestCase):

    def test_questions_paginate(self):
        QuestionFactory.create_batch(size=settings.QUESTIONS_PER_PAGE * 2)
        response = self.client.get(reverse('questions:index'))
        self.assertIn('page_obj', response.context)
        self.assertEqual(settings.QUESTIONS_PER_PAGE, len(response.context['page_obj'].object_list))

    def test_question_view_answers_paginate(self):
        question = QuestionFactory()
        AnswerFactory.create_batch(size=settings.ANSWERS_PER_PAGE * 2, question=question)
        response = self.client.get(reverse('questions:detail', kwargs={'pk': question.pk}))
        self.assertIn('page_obj', response.context)
        self.assertEqual(settings.ANSWERS_PER_PAGE, len(response.context['page_obj'].object_list))
