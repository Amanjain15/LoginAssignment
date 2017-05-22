from django.contrib import admin
from .models import *

# Register your models here.

class user_dataAdmin(admin.ModelAdmin):
	list_display= ["id","name","mobile","email","created", "modified"]
	class Meta:
		model = user_data
		
admin.site.register(user_data,user_dataAdmin)