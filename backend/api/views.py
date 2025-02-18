# Standard library imports
import os
import asyncio
from pprint import pprint

# Django imports
from django.contrib.auth import get_user_model
from django.utils import timezone
import django.core.serializers
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# Third-party library imports
import mercadopago
from google.auth.transport import requests
from google.oauth2 import id_token
from allauth.socialaccount.models import SocialAccount

# Project-specific imports
from backend.settings import SOCIAL_AUTH_GOOGLE_CLIENT_ID
from .models import PaymentTicket, Client
from .permissions import *
from .serializers import ClientSerializer, TicketSerializer


User = get_user_model()

GOOGLE_CLIENT_ID = SOCIAL_AUTH_GOOGLE_CLIENT_ID


class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("credential")
        print(f"data: {request.data}")
        print(f"token credential: {token}")

        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify ID token with Google
            google_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

            print(f'google info: {google_info}')

            email = google_info.get("email")
            google_uid = google_info.get("sub")  # Unique Google user ID
            name = google_info.get("name")
            picture = google_info.get("picture")

            if not email:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user exists or create one
            user, created = User.objects.get_or_create(email=email, defaults={"username": name})

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "message": "User authenticated successfully",
                "user_id": user.id,
                "access_token": access_token,
                "refresh_token": str(refresh),
                "name": name,
                "email": email,
                "picture": picture,
            }, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"error": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)


def updateExistingPasses(client: Client) -> None:
    client_tickets_in_use = PaymentTicket.objects.filter(owner=client, is_expired=False).order_by('-expire_time')
    for ticket in client_tickets_in_use:
        if timezone.now().date() > ticket.expire_time:
            ticket.is_expired = True
            ticket.save()
        elif ticket.amount_of_uses_LEFT == 0:
            ticket.is_expired = True
            ticket.save()


def discountClientOnePass(client: Client, type_of_service: str) -> PaymentTicket:
    client_tickets_in_use = PaymentTicket.objects.filter(owner=client,
                                                         is_expired=False,
                                                         type_of_service=type_of_service).order_by('-expire_time')
    for ticket in client_tickets_in_use:
        if ticket.amount_of_uses_LEFT > 0:
            ticket.amount_of_uses_LEFT = ticket.amount_of_uses_LEFT - 1
            ticket.save()
            return ticket
    return None


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
    permission_classes = [IsAuthenticated, IsOwnerReadOnlyOrisAdmin]

    def get_queryset(self):
        user = self.request.user
        return PaymentTicket.objects.filter(owner=user)


class ClientsViewList(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny, AdminGetAnyPost]


class ClientsViewDetail(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsOwnerReadOnlyOrisAdmin]

    def list(self, request, *args, **kwargs):
        user_profile = Client.objects.get(pk=request.user.pk)
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        type_of_service = request.data.get("type_of_service")
        client = self.get_object()

        updateExistingPasses(client)

        available_passes = discountClientOnePass(client, type_of_service)
        if available_passes:
            return Response({
                "Action": "Pass",
                "Ticket_used": django.core.serializers.serialize('json', [available_passes])
            }, status=status.HTTP_200_OK)
        else:
            return Response({"Action": "No passes left"}, status=status.HTTP_200_OK)


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
        type_of_service = request.data.get("type_of_service")
        client = self.get_object()

        updateExistingPasses(client)

        available_passes = discountClientOnePass(client, type_of_service)
        if available_passes:
            return Response({
                "Action": "OK",
                "Ticket_used": django.core.serializers.serialize('json', [available_passes])
            }, status=status.HTTP_200_OK)
        else:
            return Response({"Action": "No passes left"}, status=status.HTTP_200_OK)

class MercadoPagoTicket(ModelViewSet):
    queryset = PaymentTicket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        sdk = mercadopago.SDK(os.environ.get('MP_ACCES_TOKEN'))

        ticket_data = {
            "type_of_service": str(request.data.get("type_of_service")),
            "amount_of_uses": str(request.data.get("amount_of_uses")),
            "amount_of_uses_LEFT": str(request.data.get("amount_of_uses")),
            "owner": str(request.user.pk),
            "is_expired": True,
            "price": int(request.data.get("price")),
            "left_to_pay": int(request.data.get("price")),
            "status": "unpaid"

        }

        preference_data = {
            "items": [
                {
                    "title": f"Pass for: {ticket_data.get('type_of_service')}",
                    "quantity": 1,
                    "unit_price": int(request.data.get("price")),
                }
            ],
            "auto_return": "approved",
            "redirect_urls": {
                'failure': 'https://crm-frontend-ywqp.onrender.com/',
                'pending': 'https://www.yahoo.com.ar/',
                'success': 'https://crm-frontend-ywqp.onrender.com/'
            },
            "back_urls": {
                'failure': 'https://crm-frontend-ywqp.onrender.com/',
                'pending': 'https://www.yahoo.com.ar/',
                'success': 'https://crm-frontend-ywqp.onrender.com/'
            },
            "notification_url": 'https://crm-udrl.onrender.com/api/mercadopago/succes-hook/',
        }

        async def get_preference():
            return await asyncio.to_thread(sdk.preference().create, preference_data)

        preference_response = asyncio.run(get_preference())  # Espera la respuesta de MercadoPago

        preference = preference_response.get("response")

        pprint("preference")
        pprint(preference)

        if not preference:
            return Response({"error": "No se pudo obtener la preferencia de pago"}, status=status.HTTP_400_BAD_REQUEST)

        init_point = preference.get("init_point")
        purchase_id = preference.get("id")

        if init_point:
            ticket_data.update({"order_id": purchase_id})

            ticket_serializer = self.get_serializer(data=ticket_data)
            if ticket_serializer.is_valid():
                self.perform_create(ticket_serializer)
                return Response({"init_point": init_point, "id": purchase_id}, status=status.HTTP_201_CREATED)
            else:
                return Response(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Error al procesar el pago"}, status=status.HTTP_400_BAD_REQUEST)


class MercadoPagoSuccesHook(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        pprint(request.data)

        sdk = mercadopago.SDK(os.environ.get('MP_ACCES_TOKEN'))
        merchant_order_id = request.query_params.get("id")

        if not merchant_order_id:
            return Response({"error": "No order ID found"}, status=status.HTTP_400_BAD_REQUEST)

        order_data_raw = sdk.merchant_order().get(merchant_order_id)
        order_data = order_data_raw.get("response")
        order_id_from_ticket = order_data.get("preference_id")

        pprint('Merchant Order')
        pprint(order_data)

        if order_data.get('order_status') == 'paid':
            print("Ticket paid!")
            print("$: " + str(order_data.get("paid_amount")))

            try:
                ticket = PaymentTicket.objects.get(order_id=order_id_from_ticket)
            except PaymentTicket.DoesNotExist:
                return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

            ticket.left_to_pay -= int(order_data.get("paid_amount", 0))

            if ticket.left_to_pay <= 0:
                ticket.left_to_pay = 0
                ticket.status = "in_use"
                ticket.is_expired = False

            ticket.save()

            print("TICKET DATA", ticket)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_202_ACCEPTED)
