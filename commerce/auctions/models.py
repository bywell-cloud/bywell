from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta



class User(AbstractUser):
    email = models.CharField(max_length=200, null =True )
    phone = models.IntegerField(null = True)
       

class Category(models.Model):
    name = models.CharField(max_length=200 , db_index = True)
    slug = models.SlugField(max_length =200 , unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']
        
    
    def __str__(self):
        return  self.slug
        
  #  def get_url(self) :
  #     return reverse( 'auctions:category_list' , args=[self.slug])

class List(models.Model) :
    p_name        = models.CharField(max_length=200)
    p_description = models.TextField(max_length=700)
    image         = models.ImageField(null = True, upload_to ='images/'   , default="images/noimage.jpg"  )
    category      = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, related_name="auctions" )
    
    period = (
        (1, "1 Day"),
        (3, "3 Days"),
        (7, "1 Week")
    )

    p_period      = models.IntegerField(choices=period , default = 1)
    #ended_manually   = models.BooleanField(default=False)
    bid           = models.FloatField()
    start_time    = models.DateTimeField(auto_now_add=False )
    end_time      = models.DateTimeField(null=True)  
    close        = models.BooleanField(default=False)                   
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="list")
    p_slug        = models.SlugField(max_length=200 , null = True)
    status = models.BooleanField(default=True)
    bidder = models.ForeignKey(User, on_delete=models.SET("(deleted)"),
                               blank=True, 
                               null=True,
                               related_name="winner",
                               )


                               


    class Meta:
        ordering = ['-end_time']
        
    def __str__(self):
        return self.p_name

class Comment(models.Model):
    date = models.DateTimeField(auto_now=True)
    body = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(List, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        
        return f"Of {self.user.username} on {self.listing.p_name}"
    



class Whistlistx(models.Model):

    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wlistings = models.ForeignKey(List,on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"Of {self.user.username} on {self.wlistings} "              

class Bid(models.Model):
    price = models.FloatField()
    date = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ubids")
    listing = models.ForeignKey(
        List, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.user.username} to {self.listing.p_name}"



    