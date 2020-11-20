from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
class Style(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    style = models.BooleanField('Style', default=False)

    def __str__(self):
        return self.user.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField('Фотка', upload_to='avatars', default='avatars/avatar.png')
    phone = models.CharField('Телефон', max_length=15, default='')

    def get_absolute_url(self):
        return f'edit/{self.user.username}'

    def __str__(self):
        return self.user.username

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()