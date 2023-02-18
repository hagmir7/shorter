from django.db import models
from django.utils.crypto import get_random_string


class IpAddress(models.Model):
    pass

class Link(models.Model):
    original = models.CharField(max_length=1000)
    hash = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=30, null=True, blank=True)




    def save(self, *args, **kwargs):
        if not self.hash:
            random_str = get_random_string(length=5).upper()
            self.hash = f"https://agmir.link/{random_str}"
            self.slug = random_str
        return super(Link, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.hash
