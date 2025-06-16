from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
	age= models.IntegerField()
	budget= models.IntegerField()
	REQUIRED_FIELDS= ["age", "budget"]
