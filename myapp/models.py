from django.contrib.auth.models import User
from django.db import models
import sqlite3
from django.db.models.signals import post_save
from django.dispatch import receiver


class Stock(models.Model):
	""" the Stock's model is used to create stocks for the project use """
	symbol = models.CharField(max_length=12, primary_key=True)
	name = models.CharField(max_length=64)
	top_rank = models.IntegerField(null=True)
	price = models.FloatField()
	change = models.FloatField(null=True)
	change_percent = models.FloatField()
	market_cap = models.FloatField(null=True)
	primary_exchange = models.CharField(null=True, max_length=32)

class Profile(models.Model):
	""" the user's profile model - created automatically by sending a signal when the user is created"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg',upload_to='profile_pics')
	job = models.CharField(max_length=20, null=True, default=None)

	def __str__(self):  # __unicode__ for Python 2
		return self.user.username
	

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()
	
	
#comment model
class Comment(models.Model):
	"""
	This is the comment model. It includes : stock, author, text and created_date.
	"""
	stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='comments')
	author = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return self.text
	
class Notification(models.Model):
	"""Notification model"""
	notification_id = models.AutoField(primary_key=True)
	stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='stock_symbol')
	message = models.TextField()
	read = models.BooleanField(default=False)
	created_date = models.DateTimeField(auto_now_add=True, blank=True)

class FollowedStocks(models.Model):
	"""Stocks followed model"""
	stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='followed_stocks')
	user_id = models.CharField(max_length=10)

