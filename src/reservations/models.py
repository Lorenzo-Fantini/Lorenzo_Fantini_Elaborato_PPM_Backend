from django.db import models
from django.conf import settings
from events.models import Event

class Reservation(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL , on_delete= models.CASCADE)
    event= models.ForeignKey(Event, on_delete= models.CASCADE)
    num_tickets= models.PositiveIntegerField(default= 1)
    
    class Meta:
        unique_together= (
    		("user", "event"),
    	)