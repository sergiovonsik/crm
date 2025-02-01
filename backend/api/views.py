from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import ClientSerializer, TicketSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import isOwnerReadOnlyOrisAdmin, IsAdmin
from .models import PaymentTicket, Client
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView

class PaymentTicketList(ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PaymentTicket.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class PaymentTicketDetail(ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, isOwnerReadOnlyOrisAdmin]

    def get_queryset(self):
        user = self.request.user
        return PaymentTicket.objects.filter(author=user)


class ClientsViewList(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny, IsAdmin]

class ClientsViewDetail(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, isOwnerReadOnlyOrisAdmin]
