from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "ID: {ID}".format(
            ID=self.user_id
        )


class Image(models.Model):
    bytes = models.TextField()
    taken_on = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return "user id: ##. Image: {BYTES}  |  taken_on: {TIME}".format(
            # USER=self.user_,
            BYTES=self.bytes,
            TIME=self.taken_on
        )


class Stool(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    # the stool type based on Bristol Stool Chart
    bristol_type = models.TextField()

    # the date the person pooped
    date = models.DateTimeField()

    contains_blood = models.BooleanField()

    contains_mucus = models.BooleanField()

    # color distribution of percentage and RGB colors
    color_distribution = models.TextField()

    # bytes of color distribution bar chart of your stool
    bar_chart = models.TextField()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()