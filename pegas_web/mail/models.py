from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class File(models.Model):
    file = models.FileField(upload_to="files/", default=None, blank=True, null=True)
    # def get_absolute_url(self):
    #     return reverse('mail:document-detail', kwargs={'pk': self.pk})


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", default=None)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver", default=None, blank=True,
                                 null=True)
    topic = models.CharField(max_length=700)
    text_message = models.TextField()
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    files = models.ManyToManyField(File, related_name="files", default=None, blank=True)
    draft = models.BooleanField(default=False, blank=True, null=True)
    is_deleted = models.BooleanField(default=False, blank=True, null=True)
    is_truly_deleted = models.BooleanField(default=False, blank=True, null=True)
    is_favourite = models.BooleanField(default=False, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("message_detail", kwargs={"pk": self.id})

    class Meta:
        ordering = ['-date']
