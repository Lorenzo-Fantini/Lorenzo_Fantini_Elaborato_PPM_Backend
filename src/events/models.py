from django.db import models

class Event(models.Model):
    AGE_CATEGORIES = (
        (0, "everybody"),
        (14, "teens"),
        (18, "adults"),
    )
    title = models.CharField(max_length=20, primary_key=True)
    description = models.TextField()
    location = models.CharField(max_length=20)
    date_and_time = models.DateTimeField()
    ticket_price = models.IntegerField()
    available_tickets = models.IntegerField()
    age = models.IntegerField(choices=AGE_CATEGORIES, default="everybody")

