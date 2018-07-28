
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserProfileInfo(models.Model):
	user = models.OneToOneField(User)
	portfolio_site = models.URLField(blank=True)
	profile_pic = models.ImageField(upload_to = 'profile_pics',blank = True )


	def __str__(self):
		return self.user.username




#========================= Parameters ==============================

class Parameters(models.Model):
	infection_rate = models.FloatField(null = True)
	recovery_rate  = models.FloatField(null = True)
	upload_file    = models.FileField(upload_to = 'profile_pics' , blank = False)




#======================= Simulation ===============================


class SIR(models.Model):
	lat = models.FloatField(null = True)
	lng = models.FloatField(null = True)
	counter = models.IntegerField(null = True)
	date = models.DateField(auto_now = False)

	
