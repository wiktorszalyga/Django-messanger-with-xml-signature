from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):

    private_key = models.BinaryField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.username


class Message(models.Model):
    topic = models.CharField(max_length=100, blank=False, null=False, default='Topic')
    text = models.CharField(max_length=300, blank=True, null=True)
    contain = models.FileField(upload_to='documents/', blank=True, null=True)
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='sender')
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='reciver')
    was_verify = models.BooleanField(blank=False, null=False, default=False)
    is_correct = models.BooleanField(blank=False, null=False, default=False)
    sign_data = models.BinaryField(blank=True, null=True)

    def get_absolute_url(self):
        return f"/incoming/{self.id}/"


class Key(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, blank=False, null=False)
    public_key = models.BinaryField(unique=True, blank=False, null=False)


class Permission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,unique=False, on_delete=models.CASCADE, blank=False, null=False)
    user_key = models.ForeignKey(Key, on_delete=models.CASCADE, unique=False, null=False, blank=False)

    class Meta:
        unique_together = (('user', 'user_key'),)
