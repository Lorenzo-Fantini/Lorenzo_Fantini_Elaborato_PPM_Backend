from rest_framework import serializers
from .models import Event
from datetime import date

class GetEventSerializer(serializers.ModelSerializer):
	class Meta:
		model= Event
		fields= (
			"title",
			"age",
		)
		
class DetailEventSerializer(serializers.ModelSerializer):
	class Meta:
		model= Event
		fields= (
			"title",
			"description",
			"location",
			"date_and_time",
			"ticket_price",
			"available_tickets",
			"age",
		)
		
class CreateEventSerializer(serializers.ModelSerializer):
	class Meta:
		model= Event
		fields= (
			"title",
			"description",
			"location",
			"date_and_time",
			"ticket_price",
			"available_tickets",
			"age",
		)
		
		def validate(self, attrs):
			if attrs.get("date_and_time") <= date.today():
				raise serializers.ValidationError({"date": "Invalid date"})
			if attrs.get("date_and_time") is None or attrs.get("date_and_time") == "":
				raise serializers.ValidationError({"date": "You must enter a date"})
			if attrs.get("ticket_price") <= 0:
				raise serializers.ValidationError({"ticket_price": "Invalid value"})
			if attrs.get("ticket_price") is None:
				raise serializers.ValidationError({"ticket_price": "You must enter a ticket price"})
			if attrs.get("available_tickets") <= 0:
				raise serializers.ValidationError({"available_tickets": "Invalid value"})
			if attrs.get("available_tickets") is None:
				raise serializers.ValidationError({"available_tickets": "You must enter "
																		"a number of available tickets"})
			return attrs
			
		def create(self, validated_data):
			event= Event.objects.create(**validated_data)
			return event