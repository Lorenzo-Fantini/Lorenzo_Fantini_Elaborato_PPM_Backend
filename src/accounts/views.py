from django.shortcuts import render
from rest_framework import generics
from .serializers import RegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

User = get_user_model()

# Create your views here.

class UserCreateAPIView(generics.CreateAPIView):
	queryset= User.objects.all()
	serializer_class= RegistrationSerializer
	
class UserDeleteAPIView(generics.DestroyAPIView):
	authentication_classes= [
		TokenAuthentication,
	]
	permission_classes= [
		IsAuthenticated,
	]
	
	def get_object(self):
		# Always returns the instance of the currently authenticated user.
		return self.request.user

	def perform_destroy(self, instance):
		# Add any additional pre-deletion logic here if needed.
		instance.delete()
