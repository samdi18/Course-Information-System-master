from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse




# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default= timezone.now)
    author = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.title


class Group(models.Model):
    course_name = models.CharField(max_length=100)
    course_description = models.TextField()
    password = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.course_name

    def get_absolute_url(self):
        return reverse('group', kwargs={'pk': self.pk})


class Schedule(models.Model):
    group = models.ForeignKey(Group, on_delete= models.CASCADE)
    exam = models.CharField(max_length=100)
    date = models.DateField(verbose_name='Date', auto_now_add=False, auto_now=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    objects = models.Manager()

    def __str__(self):
        return self.exam

    def get_absolute_url(self):
        return reverse('group', kwargs={'pk': self.pk})


class Announcement(models.Model):
    group = models.ForeignKey(Group, on_delete= models.CASCADE)
    subject = models.CharField(max_length=170)
    content = models.TextField(max_length=350)
    created = models.DateTimeField(auto_now_add= True)
    objects = models.Manager()

    def __str__(self):
        return self.subject
    

class Document(models.Model):
    group = models.ForeignKey(Group, on_delete= models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    group = models.ForeignKey(Group, on_delete= models.CASCADE)
    body = models.TextField(max_length=350)
    email = models.EmailField(max_length=100)
    created = models.DateTimeField(default = timezone.now)
    approved = models.BooleanField(default=False)
    objects = models.Manager()

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.email

    