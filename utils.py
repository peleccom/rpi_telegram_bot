import logging

from six import wraps

from settings import Settings

logger = logging.getLogger(__name__)

settings = Settings()


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        list_of_admins = settings.get_value('LIST_OF_ADMINS')
        user_id = update.effective_user.id
        if user_id not in list_of_admins:
            logging.warning("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)

    return wrapped
