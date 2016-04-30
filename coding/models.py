from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class myUser(models.Model):
    user = models.OneToOneField(User, related_name='myuser')
    codechef_handle = models.CharField(max_length=200)
    spoj_handle = models.CharField(max_length=200)
    codeforces_handle = models.CharField(max_length=200)
    problem_count = models.IntegerField(default=0)
    spoj_count = models.IntegerField(default=0)
    codeforces_count = models.IntegerField(default=0)
    codechef_count = models.IntegerField(default=0)
    def __str__(self):
		return self.user.username


class PastContest(models.Model):
    platform = models.CharField(max_length=200)
    start_time = models.CharField(max_length=200)
    end_time = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    #date = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    
    def __str__(self):
		return self.name	


class UpcomingContest(models.Model):
    platform = models.CharField(max_length=200)
    start_time = models.CharField(max_length=200)
    end_time = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    #date = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name   

class OngoingContest(models.Model):
    platform = models.CharField(max_length=200)
    #start_time = models.CharField(max_length=200)
    end_time = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    #date = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name                    
    
