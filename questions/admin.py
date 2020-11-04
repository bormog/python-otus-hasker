from django.contrib import admin
from .models import Question, Tag, Answer, Vote

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date_pub', 'rank')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('content', 'question', 'user', 'is_right', 'date_pub', 'rank')

class VoteAdmin(admin.ModelAdmin):
    list_display = ('vote', 'user', 'content_type', 'object_id', 'content_object')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Tag)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Vote, VoteAdmin)
