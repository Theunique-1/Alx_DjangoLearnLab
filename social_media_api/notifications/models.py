from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actor_notifications')
    verb = models.CharField(max_length=255)
    target_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    target_id = models.PositiveIntegerField(null=True)
    target = GenericForeignKey('target_type', 'target_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def _str_(self):
        return self.verb