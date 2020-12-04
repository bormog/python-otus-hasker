from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete


class VotesConfig(AppConfig):
    name = 'votes'

    def ready(self):
        from .models import Vote
        from .receivers import after_like_save_callback

        post_save.connect(after_like_save_callback, sender=Vote, dispatch_uid='after_like_save')
        post_delete.connect(after_like_save_callback, sender=Vote, dispatch_uid='after_like_delete')
