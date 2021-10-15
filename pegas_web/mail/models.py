from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class File(models.Model):
    file=models.FileField(upload_to="files/", default=None, blank=True, null=True)
    # def get_absolute_url(self):
    #     return reverse('mail:document-detail', kwargs={'pk': self.pk})


class Message(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender", default=None)
    receiver=models.ForeignKey(User, on_delete=models.CASCADE,related_name="receiver", default=None,blank=True,null=True)
    topic=models.CharField(max_length=700)
    text_message= models.TextField()
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    files = models.ManyToManyField(File, related_name="files", default=None, blank=True)
    draft = models.BooleanField(default=False, blank=True,null=True)

    def get_absolute_url(self):
        return reverse("message_detail", kwargs={"pk": self.id})
<<<<<<< Updated upstream
=======

class Road(models.Model):
    creator=models.ForeignKey(User,on_delete=models.CASCADE,related_name="creator", default=None)
    date_creation = models.DateTimeField(auto_now_add=True, auto_now=False)
    # user_route = models.ManyToManyField(User, related_name="user_roat")

class UserInRoute(models.Model):
    route = models.ForeignKey(Road,on_delete=models.CASCADE,related_name="road", default=None)
    prevus = models.ForeignKey(User,on_delete=models.CASCADE,related_name="prevus", default=None)
    nextus = models.ForeignKey(User,on_delete=models.CASCADE,related_name="nextus", default=None, blank=True, null=True)
    u_sequence = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        ordering = ['id',]

class RouteMessageJournal(models.Model):
    prev_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="prev_user", default=None)
    next_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="next_user", default=None)
    message_id = models.ForeignKey(Message,on_delete=models.CASCADE,related_name="message_id", default=None)
    route_id = models.ForeignKey(Road,on_delete=models.CASCADE,related_name="road_id", default=None)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)


class Tags(models.Model):
    tag = models.CharField(max_length=20)
    name_tag = models.CharField(max_length=50)

class Templates(models.Model):
    title = models.CharField(max_length=300)
    file = models.FileField()
    tags = models.ManyToManyField(Tags, related_name="tags", default=None, blank=True)

    def get_absolute_url(self):
        return reverse("template_detail", kwargs={"pk": self.id})


>>>>>>> Stashed changes
