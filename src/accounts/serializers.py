from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
	class Meta:
		model= User
		fields= [
			"username",
			"password",
			"age",
			"budget",
		]
		
	def validate(self, attrs):
		if User.objects.filter(username= attrs.get("username")).exists():
			raise serializers.ValidationError({"username": "Username already exists"})
		if attrs.get("username") is None or attrs.get("username") == "":
			raise serializers.ValidationError({"username": "You must enter a username"})
		if attrs.get("age") < 0 or attrs.get("age") > 122:
			raise serializers.ValidationError({"age": "Invalid age"})
		if attrs.get("age") is None:
			raise serializers.ValidationError({"age": "You must enter an age"})
		if attrs.get("budget") <= 0:
			raise serializers.ValidationError({"budget": "Invalid budget"})
		if attrs.get("budget") is None:
			raise serializers.ValidationError({"budget": "You must enter a budget"})
		return attrs
		
	def create(self, validated_data):
		user= User.objects.create_user(**validated_data)
		return user