from django.shortcuts import render
from rest_framework import generics
from .serializers import RegistrationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class UserCreateAPIView(generics.CreateAPIView):
	queryset= User.objects.all()
	serializer_class= RegistrationSerializer
	
class UserDeleteAPIView(generics.DestroyAPIView):
	queryset= User.objects.all()
	lookup_field= "username"
	permission_classes= [
		IsAuthenticated
	]
	
	def perform_destroy(instance):
		super.perform_destroy(instance)
