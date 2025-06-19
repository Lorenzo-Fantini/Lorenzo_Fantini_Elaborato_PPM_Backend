from .serializers import (ListReservationSerializer, CreateReservationSerializer,
						  UpdateReservationSerializer, DeleteReservationSerializer)
from .models import Reservation
from transactions.models import Transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from django.db import transaction

# Create your views here.

class UserReservationListAPIView(generics.ListAPIView):
	queryset= Reservation.objects.all()
	serializer_class= ListReservationSerializer
	authentication_classes= [
		TokenAuthentication
	]
	permission_classes= [
		IsAuthenticated,
	]
	
	def get_queryset(self):
		qs = super().get_queryset()
		return qs.filter(user=self.request.user)

class UserReservationCreateAPIView(generics.CreateAPIView):
	queryset= Reservation.objects.all()
	serializer_class= CreateReservationSerializer
	authentication_classes= [
		TokenAuthentication
	]
	permission_classes= [
		IsAuthenticated,
	]

	@transaction.atomic
	def perform_create(self, serializer):
		user = self.request.user
		event = serializer.validated_data['event']
		num_tickets = serializer.validated_data['num_tickets']
		total_cost = num_tickets * event.ticket_price

		event.available_tickets -= num_tickets
		event.save(update_fields=["available_tickets"])

		user.budget -= total_cost
		user.save(update_fields=["budget"])

		serializer.save(user=user)

		Transaction.objects.create(
			user=user,
			event=event,
			amount=total_cost,
			num_tickets=num_tickets
		)


class UserReservationUpdateAPIView(generics.UpdateAPIView):
	queryset= Reservation.objects.all()
	serializer_class= UpdateReservationSerializer
	authentication_classes= [
		TokenAuthentication
	]
	permission_classes= [
		IsAuthenticated,
	]
	lookup_field= "event"

	@transaction.atomic
	def perform_update(self, serializer):
		reservation = self.get_object()
		user = self.request.user
		event = reservation.event
		old_num_tickets = reservation.num_tickets
		new_num_tickets = serializer.validated_data['num_tickets']
		delta_tickets = new_num_tickets - old_num_tickets
		delta_cost = delta_tickets * event.ticket_price

		event.available_tickets -= delta_tickets
		user.budget -= delta_cost

		event.save(update_fields=['available_tickets'])
		user.save(update_fields=['budget'])
		serializer.save()

		Transaction.objects.create(
			user=user,
			event=event,
			amount=delta_cost,
			num_tickets=delta_tickets
		)

class UserReservationDeleteAPIView(generics.DestroyAPIView):
	queryset= Reservation.objects.all()
	serializer_class = DeleteReservationSerializer
	authentication_classes= [
		TokenAuthentication
	]
	permission_classes= [
		IsAuthenticated,
	]
	lookup_field = "event"

	@transaction.atomic
	def perform_destroy(self, instance):
		reservation= self.get_object()
		user = self.request.user
		event = reservation.event

		event.available_tickets += reservation.num_tickets
		user.budget += event.ticket_price * reservation.num_tickets

		event.save(update_fields=['available_tickets'])
		user.save(update_fields=['budget'])
		reservation.delete()

		Transaction.objects.create(
			user=user,
			event=event,
			amount= -(event.ticket_price * reservation.num_tickets),
			num_tickets= -reservation.num_tickets
		)
