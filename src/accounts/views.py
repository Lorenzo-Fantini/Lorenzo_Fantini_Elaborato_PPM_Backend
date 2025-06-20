from rest_framework.response import Response
from rest_framework import generics
from .serializers import RegistrationSerializer
from reservations.models import Reservation
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

User = get_user_model()

# Create your views here.

class UserCreateAPIView(generics.CreateAPIView):
	queryset= User.objects.all()
	serializer_class= RegistrationSerializer

class UserGetBudgetAPIView(generics.RetrieveAPIView):
	authentication_classes= [
		TokenAuthentication,
	]
	permission_classes= [
		IsAuthenticated,
	]

	def get(self, request, *args, **kwargs):
		budget= request.user.budget
		return Response({"budget": budget})
	
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
		reservations = Reservation.objects.filter(user=instance)
		for reservation in reservations:
			event = reservation.event
			event.available_tickets += reservation.num_tickets
			event.save(update_fields=['available_tickets'])

		reservations.delete()
		instance.delete()
