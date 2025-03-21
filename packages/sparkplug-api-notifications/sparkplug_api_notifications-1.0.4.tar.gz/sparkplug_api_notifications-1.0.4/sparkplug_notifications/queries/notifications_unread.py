# django
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import QuerySet

# app
from ..models import Notification


def notifications_unread(
    recipient: type[AbstractBaseUser],
) -> QuerySet["Notification"]:
    return (
        Notification.objects
        .filter(recipient=recipient)
        .filter(read=False)
    )
