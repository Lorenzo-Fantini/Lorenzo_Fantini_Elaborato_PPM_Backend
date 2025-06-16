from rest_framework import serializers
from .models import Reservation
from events.models import Event
from datetime import date
from django.contrib.auth import get_user_model

User= get_user_model()

class ListReservationSerializer(serializers.ModelSerializer):
	class Meta:
		model= Reservation
		fields= (
			"user",
			"event",
			"num_tickets",
		)
		
		def validate_num_tickets(self, num_tickets_value):
			if num_tickets_value > 10:
				raise serializers.ValidationError({"tickets": "Too many tickets"})
			if num_tickets_value <= 0:
				raise serializers.ValidationError({"tickets": "Invalid number of tickets"})
			return num_tickets_value
			
class UpdateReservationSerializer(serializers.ModelSerializer):
	class Meta:
		model= Reservation
		fields= (
			"num_tickets",
		)
			
class CreateReservationSerializer(serializers.ModelSerializer):
	user= serializers.SlugRelatedField(
        queryset= User.objects.all(),
        slug_field= 'username'
    )
	
	class Meta:
		model= Reservation
		fields= (
			"user",
			"event",
			"num_tickets",
		)
		
		def validate(self, data):
			request = self.context.get("request")
			user= request.user
			event= data.get("event")
			event_id= Event.objects.filter(name= event)
			user_age= User.objects.filter(username= user)
			event_age= Event.object.filter(title= event)
			
			if Reservation.objects.filter(event= event_id).exists():
				raise serializers.ValidationError({"event": "Reservation for that event already exists"})
			if user_age < event_age:
				raise serializers.ValidationError({"user": "You're too young to make a reservation for this event"})
			return data
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
