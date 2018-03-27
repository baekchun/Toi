from django.db import models

class Image(models.Model):
    bytes = models.TextField()
    taken_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{BYTES}__image_taken_on: {TIME}".format(
            BYTES=self.bytes,
            TIME=self.taken_on
        )