from django import forms
from django.core.exceptions import ValidationError

from .models import Question, Tag, Answer, Vote


class CommaSeparatedTextField(forms.Field):
    widget = forms.TextInput()

    def to_python(self, value):
        tags = []
        if value:
            values = [i.lower() for i in map(str.strip, value.split(',')) if i]
            if len(values) <= 3:
                for tag_name in values:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    tags.append(tag)
                return tags
            else:
                raise ValidationError('Max 3 tags is allowed')
        return tags


class QuestionAddForm(forms.ModelForm):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea, label='Your Question')
    tags = CommaSeparatedTextField(required=False)

    class Meta:
        model = Question
        fields = ('title', 'content', 'tags')


class AnswerAddForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='Your Answer')

    class Meta:
        model = Answer
        fields = ('content',)


class VoteForm(forms.Form):
    object_type_choices = (
        (Question._meta.model_name, Question),
        (Answer._meta.model_name, Answer)
    )
    vote_choices = (
        ('like', Vote.VOTE_LIKE),
        ('dislike', Vote.VOTE_DISLIKE)
    )
    object_type = forms.ChoiceField(choices=object_type_choices)
    object_id = forms.IntegerField()
    vote = forms.ChoiceField(choices=vote_choices)

    def clean(self):
        cleaned_data = super().clean()
        object_type = cleaned_data.get('object_type')
        object_id = cleaned_data.get('object_id')
        if object_type and object_id:
            print(object_type)
            print(self.fields['object_type'])
            #msg = 'Hello World'
            #self.add_error('object_id', msg)

