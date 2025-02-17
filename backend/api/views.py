from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
import os
import django.core.serializers
from backend.settings import SOCIAL_AUTH_GOOGLE_CLIENT_ID
from .serializers import ClientSerializer, TicketSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import *
from .models import PaymentTicket, Client
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.generics import ListCreateAPIView
from django.utils import timezone
import mercadopago
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from pprint import pprint

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


def discountClientOnePass(client: Client, type_of_service: str) -> bool:
    client_tickets_in_use = PaymentTicket.objects.filter(owner=client,
                                                         is_expired=False,
                                                         type_of_service=type_of_service).order_by('-expire_time')
    for ticket in client_tickets_in_use:
        if ticket.amount_of_uses_LEFT > 0:
            ticket.amount_of_uses_LEFT = ticket.amount_of_uses_LEFT - 1
            ticket.save()
            return ticket
    return False


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
        sdk = mercadopago.SDK("APP_USR-2423666870753668-020510-302e22177e1c6d6c30c3e8a9b20f1f35-2247408635")
        """
        Public_Key = 'APP_USR-d69ae28c-5036-428e-9440-6fc15a8cf194'
        Access_Token = 'APP_USR-2423666870753668-020510-302e22177e1c6d6c30c3e8a9b20f1f35-2247408635' 
        """

        ticket_data = dict(
            type_of_service=str(request.data.get("type_of_service")),
            amount_of_uses=str(request.data.get("amount_of_uses")),
            owner=str(request.user.pk),
            is_expired=True,
        )

        preference_data = dict(
            items=[
                {
                    "title": f"Pass for: {ticket_data.get('type_of_service')}",
                    "quantity": int(request.data.get("amount_of_uses")),
                    "unit_price": int(request.data.get("price")),
                }
            ],
            auto_return="approved",
            redirect_urls={
                'failure': 'https://crm-frontend-ywqp.onrender.com/',
                'pending': 'https://www.yahoo.com.ar/',
                'success': f'https://crm-frontend-ywqp.onrender.com/'},
            back_urls={
                'failure': 'https://crm-frontend-ywqp.onrender.com/',
                'pending': 'https://www.yahoo.com.ar/',
                'success': f'https://crm-frontend-ywqp.onrender.com/'},
            notification_url=f'https://crm-udrl.onrender.com/api/mercadopago/succes-hook/',

        )
        '''
                preference_data = {
          "items": [
            {
                "id": "item-ID-1234",
                "title": "Meu produto",
                "currency_id": "BRL",
                "picture_url": "https://www.mercadopago.com/org-img/MP3/home/logomp3.gif",
                "description": "Descrição do Item",
                "category_id": "art",
                "quantity": 1,
                "unit_price": 75.76
            }
        ],
        "payer": {
            "name": "João",
            "surname": "Silva",
            "email": "user@email.com",
            "phone": {
                "area_code": "11",
                "number": "4444-4444"
            },
            "identification": {
                "type": "CPF",
                "number": "19119119100"
            },
            "address": {
                "street_name": "Street",
                "street_number": 123,
                "zip_code": "06233200"
            }
        },
        "back_urls": {
            "success": "https://www.success.com",
            "failure": "http://www.failure.com",
            "pending": "http://www.pending.com"
        },
        "auto_return": "approved",
        false,
        "notification_url": "https://www.your-site.com/ipn",
        "statement_descriptor": "MEUNEGOCIO",
        "external_reference": "Reference_1234",
        "expires": True,
        "expiration_date_from": "2016-02-01T12:00:00.000-04:00",
        "expiration_date_to": "2016-02-28T12:00:00.000-04:00"
        }
        
        '''

        preference_response = sdk.preference().create(preference_data)

        preference = preference_response.get("response")

        pprint(preference_response)

        init_point = preference.get("init_point")
        id = preference.get("id")

        if init_point is not None:
            # create ticket instance
            ticket_data["order_id"] = int(id)
            ticket_data["price"] = int(request.data.get("price"))
            ticket_data["left_to_pay"] = int(request.data.get("price"))
            ticket_data["status"] = "unpaid"

            ticket_serializer = self.get_serializer(data=ticket_data)
            ticket_serializer.is_valid()
            self.perform_create(ticket_serializer)

            return Response(dict(init_point=init_point, id=id), status=status.HTTP_201_CREATED)
        return Response(f"ERROR: {preference_response}", status=status.HTTP_400_BAD_REQUEST)


class MercadoPagoSuccesHook(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        pprint(request.query_params)
        pprint(request.data)

        sdk = mercadopago.SDK("APP_USR-2423666870753668-020510-302e22177e1c6d6c30c3e8a9b20f1f35-2247408635")
        merchant_order_id = request.query_params.get("id")
        pprint('merchant Order')
        pprint(sdk.merchant_order().get(merchant_order_id).get("response"))

        order_data = sdk.merchant_order().get(merchant_order_id).get("response")

        print("order_status " + order_data.get('order_status'))
        if order_data.get('order_status') == 'paid':
            ticket = PaymentTicket.objects.get(order_id=merchant_order_id)
            ticket.left_to_pay -= int(order_data.get("paid_amount"))
            if ticket.left_to_pay == 0:
                ticket.status = "in_use"
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_202_ACCEPTED)
