def after_like_save_callback(sender, **kwargs):
    vote_obj = kwargs['instance']
    if hasattr(vote_obj, 'on_vote_change'):
        vote_obj.on_vote_change()
