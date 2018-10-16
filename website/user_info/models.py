from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    nickname = models.CharField(max_length = 100)

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname, self.user.username)



# 只是简化profile在前端使用，编写前端可以直接使用两个方法判断

def get_nickname(self):
    if Profile.objects.filter(user = self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username

def has_nickname(self):
    return Profile.objects.filter(user = self).exists()

User.get_nickname= get_nickname
User.has_nickname= has_nickname