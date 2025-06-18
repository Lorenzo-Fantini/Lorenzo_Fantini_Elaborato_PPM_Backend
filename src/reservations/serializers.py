from rest_framework import serializers
from .models import Reservation
from django.db import transaction
from django.contrib.auth import get_user_model

User= get_user_model()

class ListReservationSerializer(serializers.ModelSerializer):
	class Meta:
		model= Reservation
		fields= (
			"event",
			"num_tickets",
		)

class CreateReservationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reservation
		fields = (
			"event",
			"num_tickets",
		)

	def validate(self, data):
		user = self.context['request'].user
		event = data.get('event')
		num_tickets = data.get('num_tickets')
		total_cost = num_tickets * event.ticket_price

		if Reservation.objects.filter(event=event.title).exists():
			raise serializers.ValidationError({"event": "Reservation for that event "
														"already exists"})
		if user.age < event.age:
			raise serializers.ValidationError({"user": "You're too young to make a "
													   "reservation for this event"})
		if event.available_tickets < num_tickets:
			raise serializers.ValidationError({"num_tickets": ("Not enough tickets available "
															  "for this event.")})
		if user.budget < total_cost:
			raise serializers.ValidationError("Insufficient budget to complete this reservation.")
		return data
			
class UpdateReservationSerializer(serializers.ModelSerializer):
	class Meta:
		model= Reservation
		fields= (
			"event",
			"num_tickets",
		)

	def validate(self, data):
		reservation= self.instance
		user = self.context['request'].user
		event = reservation.event
		old_num_tickets = reservation.num_tickets
		new_num_tickets = data.get('num_tickets')
		delta_tickets= new_num_tickets - old_num_tickets

		if new_num_tickets <= 0 or new_num_tickets > 10:
			raise serializers.ValidationError({"num_tickets": "Invalid number of tickets"})

		if delta_tickets > 0:
			delta_cost= delta_tickets * event.ticket_price
			if user.budget - delta_cost < 0:
				raise serializers.ValidationError("Insufficient budget")

		return data