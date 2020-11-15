from django.contrib import admin
from .models import Vote


class VoteAdmin(admin.ModelAdmin):
    list_display = ('vote', 'user', 'content_type', 'object_id', 'content_object')


admin.site.register(Vote, VoteAdmin)
