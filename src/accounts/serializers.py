
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
		if attrs.get("age") < 0 or attrs.get("age") > 122:
			raise serializers.ValidationError({"age": "Invalid age"})
		if attrs.get("budget") < 0:
			raise serializers.ValidationError({"budget": "Invalid budget"})
		return attrs
		
	def create(self, validated_data):
		user= User.objects.create_user(**validated_data)
		return user
