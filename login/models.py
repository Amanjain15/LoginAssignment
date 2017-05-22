from __future__ import unicode_literals

from django.db import models

# Create your models here.
class user_data(models.Model):
	id=models.AutoField(primary_key=True)
	modified = models.DateTimeField(auto_now=True, auto_now_add=False)
   	created = models.DateTimeField(auto_now=False, auto_now_add=True)
   	name=models.CharField(max_length=100,blank=True ,null= True)
	mobile=models.CharField(max_length=100,blank=False ,null= False)
	email=models.TextField(blank=False ,null= False)
	
	# def __unicode__(self):
	# 	return self.id

	# def __str__(self):
	# 	return self.id