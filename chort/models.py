from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country_flag = models.CharField(max_length=300, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    browser = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)







class Link(models.Model):
    original = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hash = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=30, null=True, blank=True)
    views = models.ManyToManyField(Location, blank=True, related_name='location')
    qr_code = models.ImageField(upload_to="QRCode", null=True, blank=True)
    custome = models.BooleanField(default=False)

        




    def save(self, *args, **kwargs):
        if not self.slug:
            random_str = get_random_string(length=5).upper()
            self.hash = f"https://frwsd.ink/{random_str}"
            self.slug = random_str
        else:
            self.hash = f"https://frwsd.ink/{self.slug}"
            


        return super().save(*args, **kwargs)

    
    def __str__(self):
        return self.hash




class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    url = models.ForeignKey(Link, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)




class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='Post', null=True, blank=True, default="d_post.webp")
    body = models.TextField()
    tags = models.CharField(max_length=150, null=True, blank=True)
    is_page = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True, unique=True)
    date = models.DateField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_random_string(length=15)
        super(Post, self).save(*args, **kwargs)




    def __str__(self):
        return self.title
        


