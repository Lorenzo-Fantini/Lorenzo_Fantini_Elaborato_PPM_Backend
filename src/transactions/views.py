from transactions.serializers import GetTransactionSerializer
from .models import Transaction
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

# Create your views here.


class TransactionListAPIView(generics.ListAPIView):
	queryset= Transaction.objects.all()
	serializer_class= GetTransactionSerializer
	authentication_classes= [
		TokenAuthentication,
	]
	permission_classes= [
        IsAdminUser,
    ]