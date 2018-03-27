from django.db import models

class Image(models.Model):
    bytes = models.TextField()
    taken_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{BYTES}__image_taken_on: {TIME}".format(
            BYTES=self.bytes,
            TIME=self.taken_on
        )


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