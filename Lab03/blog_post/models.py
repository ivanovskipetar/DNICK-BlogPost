from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="files/", blank=True, null=True)
    interests = models.CharField(max_length=100, null=True, blank=True)
    skills = models.CharField(max_length=100, null=True, blank=True)
    profession = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(BlogUser,on_delete=models.CASCADE)
    content = models.TextField()
    img = models.ImageField(upload_to="files/")
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PostComment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(BlogUser,on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Block(models.Model):
    blocker = models.ForeignKey(to=BlogUser, on_delete=models.CASCADE, related_name="user_blocker")
    blocked = models.ForeignKey(to=BlogUser, on_delete=models.CASCADE, related_name="user_blocked")

    def __str__(self):
        return str(self.blocker) + " blocked " + str(self.blocked)
