from django.contrib.auth.models import User


def is_telegram_user_registered(telegram_id):
    try:
        User.objects.get(username=str(telegram_id))
        return True
    except User.DoesNotExist:
        return False
