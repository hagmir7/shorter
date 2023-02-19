from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User


class Location(models.Model):
    ip = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country_flag = models.CharField(max_length=300, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    browser = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)








class Link(models.Model):
    original = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hash = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=30, null=True, blank=True)
    views = models.ManyToManyField(Location, blank=True, related_name='location')
    qr_code = models.ImageField(upload_to="QRCode", null=True, blank=True)

        




    def save(self, *args, **kwargs):
        if not self.hash:
            random_str = get_random_string(length=5).upper()
            self.hash = f"https://agmir.link/{random_str}"
            self.slug = random_str


        return super().save(*args, **kwargs)

    
    def __str__(self):
        return self.hash




class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    url = models.ForeignKey(Link, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

