from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='user_account',on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='cloth/profile_images', blank=True, null=True)
    token = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.user.username
    
# class ResetPasswordToken(models.Model):
#     user = models.OneToOneField(User, related_name='user_account',on_delete=models.CASCADE)
#     token = models.CharField(max_length=100, blank=True, null=True)
#     def __str__(self):
#         return self.user.username