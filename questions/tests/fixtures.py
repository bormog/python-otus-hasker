import factory

from questions.models import Question, Answer, Tag
from users.tests.fixtures import UserFactory


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: 'tag{}'.format(n))


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    title = factory.Sequence(lambda n: 'question-title{}'.format(n))
    content = factory.Sequence(lambda n: 'question-content{}'.format(n))
    user = factory.SubFactory(UserFactory)


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    question = factory.SubFactory(QuestionFactory)
    content = factory.Sequence(lambda n: 'answer-content{}'.format(n))
    user = factory.SubFactory(UserFactory)
