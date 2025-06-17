from rest_framework import serializers
from .models import Reservation
from django.db import transaction
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
		user = self.context['request'].user
		event = data.get('event')
		num_tickets = data.get('num_tickets')
		total_cost = num_tickets * event.ticket_price

		if Reservation.objects.filter(event= event.title).exists():
			raise serializers.ValidationError({"event": "Reservation for that event "
														"already exists"})
		if user.age < event.age:
			raise serializers.ValidationError({"user": "You're too young to make a "
													   "reservation for this event"})
		if event.available_tickets < num_tickets:
			raise serializers.ValidationError("Not enough tickets available for this event.")
		if user.budget < total_cost:
			raise serializers.ValidationError("Insufficient budget to complete this reservation.")
		return data

	def create(self, validated_data):
		user = self.context['request'].user
		event = validated_data['event']
		num_tickets = validated_data['num_tickets']
		total_cost = num_tickets * event.ticket_price

		with transaction.atomic():
			# Update event's available tickets
			event.available_tickets -= num_tickets
			event.save()

			# Update user's budget
			user.budget -= total_cost
			user.save()

			# Save the reservation with the authenticated user
			reservation = Reservation.objects.create(user=user, **validated_data)
		return reservation