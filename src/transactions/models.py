from django.db import models
from django.conf import settings
from events.models import Event

class Transaction(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL , on_delete= models.CASCADE)
    event= models.ForeignKey(Event, on_delete= models.CASCADE)
    num_tickets= models.IntegerField(default= 1)
    amount= models.IntegerField()