from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follower_no = models.IntegerField(default=0 , blank = True)
    following_no = models.IntegerField(default=0 , blank = True)
    follow_status = models.BooleanField(default=False)
    def __str__(self):

        return f'{self.username}'


class NewPost(models.Model):
    
    newpost = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0 , blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, blank=True, related_name="liked")
    def serialize(self):
        return {
            "id": self.id,
            "newpost": self.newpost,
            "likes": [user.newpost for user in self.likes.all()],
            
            "author": self.author.newpost,
            "created_date": self.created_date("%b %d %Y, %I:%M %p")
        }
    def __str__(self):

        return f'{self.created_date}'

    

    

class Follow(models.Model):

    follow = models.ForeignKey(User,on_delete= models.CASCADE)
    following=models.ManyToManyField(User, blank=True, related_name="following")
    follower=models.ManyToManyField(User, blank=True, related_name="follower")

    def __str__(self):

        return self.follow.username