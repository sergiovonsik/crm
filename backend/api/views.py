import django.core.serializers
from django.db.models import QuerySet
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import ClientSerializer, TicketSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import isOwnerReadOnlyOrisAdmin, IsAdmin
from .models import PaymentTicket, Client
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.utils import timezone


class PaymentTicketList(ListCreateAPIView):
    queryset = PaymentTicket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        else:
            print(serializer.errors)


class PaymentTicketDetail(ModelViewSet):
    queryset = PaymentTicket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, isOwnerReadOnlyOrisAdmin]

    def get_queryset(self):
        user = self.request.user
        return PaymentTicket.objects.filter(owner=user)


class ClientsViewList(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny, IsAdmin]


class ClientsViewDetail(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, isOwnerReadOnlyOrisAdmin]


class AdminAddPassesToClient(ModelViewSet):
    queryset = PaymentTicket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):

        type_of_service = request.data.get("type_of_service")
        amount_of_uses = request.data.get("amount_of_uses")
        client_ticket_pk = request.data.get("client_ticket_pk")
        owner = Client.objects.get(pk=client_ticket_pk)

        ticket_data = dict(type_of_service=type_of_service,
                           amount_of_uses=amount_of_uses,
                           owner={str(owner.pk)})

        ticket_serializer = self.get_serializer(data=ticket_data)

        if ticket_serializer.is_valid():
            self.perform_create(ticket_serializer)
            return Response(ticket_serializer.data, status=status.HTTP_201_CREATED)
        return Response(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminTakeAPassForClient(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def partial_update(self, request, *args, **kwargs):
        type_of_service = self.request.data.get("type_of_service")
        client = self.get_object()

        self.updateExistingPasses(client)

        available_passes = self.checkForExistingPasses(client, type_of_service)
        if available_passes:
            return Response({"Action": "OK",
                             "Ticket_used": django.core.serializers.serialize('json', [available_passes])
                             })
        else:
            return Response({"Action": "No passes Left"})

    def checkForExistingPasses(self, client: Client, type_of_service: str) -> bool:
        client_tickets_in_use = PaymentTicket.objects.filter(owner=client,
                                                             is_expired=False,
                                                             type_of_service=type_of_service).order_by('-expire_time')
        for ticket in client_tickets_in_use:
            if ticket.amount_of_uses_LEFT > 0:
                ticket.amount_of_uses_LEFT = ticket.amount_of_uses_LEFT - 1
                ticket.save()
                return ticket
        return False

    def updateExistingPasses(self, client: Client) -> None:
        client_tickets_in_use = PaymentTicket.objects.filter(owner=client, is_expired=False).order_by('-expire_time')
        for ticket in client_tickets_in_use:
            if timezone.now().date() > ticket.expire_time:
                ticket.is_expired = True
                ticket.save()
            elif ticket.amount_of_uses_LEFT == 0:
                ticket.is_expired = True
                ticket.save()
