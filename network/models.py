from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    userImage = models.FileField(upload_to='images', null=True, blank=True)
    background = models.FileField(upload_to='images', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    birth = models.DateField(null=True, blank=True)

    @property
    def get_picture_upload_user(self):
        if self.userImage and hasattr(self.userImage, 'url'):
            return self.userImage.url
    @property
    def get_picture_upload_background(self):
        if self.background and hasattr(self.background, 'url'):
            return self.background.url

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    field = models.CharField(max_length=4096)
    image = models.FileField(upload_to='images', null=True, blank=True)
    likes = models.ManyToManyField(User,  blank=True, related_name="likes")
    time = models.DateTimeField(auto_now_add=True)

    @property
    def get_picture_upload(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ManyToManyField(User,  blank=True, related_name="follower")
    following = models.ManyToManyField(User,  blank=True, related_name="following")

    def __str__(self):
        return self.user.username
