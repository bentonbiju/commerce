from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing',null = True,related_name='+',blank=True,default =None)


class Listing(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="listing")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    url = models.CharField(max_length = 1000, null = True)




class Bid(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bid_user")
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name = "bid_listing")
    bid = models.IntegerField()
    current_bidder = models.ForeignKey(User,on_delete=models.CASCADE,related_name="current_bidder",default = "benton")