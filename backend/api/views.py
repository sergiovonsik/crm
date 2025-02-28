# Standard library imports
import os
import asyncio
from pprint import pprint
from dotenv import load_dotenv

# Django imports
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import get_object_or_404
import django.core.serializers
from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.decorators import action
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
from collections import defaultdict
from itertools import groupby

# Project-specific imports
from datetime import timedelta
from backend.settings import SOCIAL_AUTH_GOOGLE_CLIENT_ID
from .models import PaymentTicket, Client
from .permissions import *
from .serializers import *

# Initialize environment variables
load_dotenv()  # Load variables from .env

# Get the MercadoPago Access Token


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
        if timezone.now().date() > ticket.expire_time or ticket.amount_of_uses_LEFT == 0:
            ticket.is_expired = True
            ticket.status = 'expired'
            ticket.save()


def discountClientOnePass(client: Client, type_of_service: str) -> PaymentTicket:
    client_tickets_in_use = PaymentTicket.objects.filter(owner=client,
                                                         is_expired=False,
                                                         type_of_service=type_of_service).order_by('-expire_time')
    print(client_tickets_in_use)
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


class Logout(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only logged-in users can log out

    def post(self, request):
        django.contrib.auth.logout(request)  # Clears the session
        return Response({"message": "Logged out successfully"}, status=200)


class UserBookingViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        client = request.user
        type_of_service = request.data.get("type_of_service")
        date = parse_date(request.data.get("date"))
        hour = request.data.get("hour")

        if not date:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        # Update and Check if user has an available ticket
        updateExistingPasses(client)

        # Check if the user already booked this date
        if Booking.objects.filter(client=client, date=date, type_of_service=type_of_service, hour=hour).exists():
            return Response({"error": "Already booked for this date"}, status=status.HTTP_400_BAD_REQUEST)

        ticket = discountClientOnePass(client, type_of_service)

        print("TICKET")
        print(ticket)
        if not ticket:
            return Response({"error": "No available tickets"}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Hour received: {hour}")  # Asegúrate de que no es None ni vacío

        booking_instance = Booking.objects.create(client=client, ticket=ticket, date=date,
                                                  type_of_service=type_of_service, hour=hour)

        return Response({"message": "Class booked successfully"}, status=status.HTTP_201_CREATED)


class UserGetHisData(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsOwnerReadOnlyOrisAdmin]

    def retrieve(self, request, *args, **kwargs):
        user_profile = request.user

        updateExistingPasses(user_profile)
        serializer = self.get_serializer(user_profile)

        return Response(serializer.data, status=status.HTTP_200_OK)


# ADMIN VIEWS

# ADMIN VIEWS FOR BUSINESS DATA

class AdminAddPassesToClient(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, isAdmin]

    def create(self, request, *args, **kwargs):
        pprint(request.data)
        type_of_service = request.data.get("type_of_service")
        amount_of_uses = request.data.get("amount_of_uses")
        user_pk = kwargs.get('pk')
        owner = get_object_or_404(Client, pk=user_pk)

        ticket_data = {
            "type_of_service": type_of_service,
            "amount_of_uses": int(amount_of_uses),
            "owner": owner.pk,
            "status": "in_use",
            "is_expired": False,
        }

        ticket_serializer = TicketSerializer(data=ticket_data)

        if ticket_serializer.is_valid():
            ticket_serializer.save()
            updateExistingPasses(owner)
            serializer = self.get_serializer(owner)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminTakeAPassForClient(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, isAdmin]

    def create(self, request, *args, **kwargs):
        client_pk = kwargs.get('pk')
        client = get_object_or_404(Client, pk=client_pk)
        type_of_service = request.data.get("type_of_service")
        date = parse_date(request.data.get("date"))
        hour = request.data.get("hour")

        updateExistingPasses(client)

        # Check for existing passes

        if Booking.objects.filter(client=client, date=date):
            return Response({'error': 'You cant create '
                                      'to Booking Tickets for the same date'},
                            status=status.HTTP_403_FORBIDDEN)

        available_passes = discountClientOnePass(client, type_of_service)
        if available_passes:

            serializer = self.get_serializer(data=dict(client=client.pk,
                                                       type_of_service=type_of_service,
                                                       ticket=available_passes.pk,
                                                       date=date))
            if serializer.is_valid():
                booking = serializer.save()
                updateExistingPasses(client)
                serializer = ClientSerializer(client).data

                return Response(serializer, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "No available passes for this client."},
                status=status.HTTP_400_BAD_REQUEST
            )


class AdminPassesChartData(APIView):
    permission_classes = [IsAuthenticated, isAdmin]

    def post(self, request, *args, **kwargs):
        try:
            start_day = parse_date(request.data.get("start_day"))
            end_day = parse_date(request.data.get("end_day"))

            passes_per_day = []

            current_date = start_day - timedelta(days=1)
            while current_date <= end_day:
                current_date = current_date + timedelta(days=1)
                passes_per_day.append(
                    dict(
                        date=str(current_date),
                        value=Booking.objects.filter(date=current_date).count(),
                        free_climb_value=Booking.objects.filter(date=current_date,
                                                                type_of_service="free_climbing").count(),
                        classes_value=Booking.objects.filter(date=current_date,
                                                             type_of_service="classes").count(),
                    )
                )

            return Response({"chart_data": passes_per_day}, status=status.HTTP_200_OK)

        except (ValueError, TypeError) as e:
            return Response({"error": "Invalid input or format", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminTicketsChartData(APIView):
    permission_classes = [IsAuthenticated, isAdmin]

    def post(self, request, *args, **kwargs):
        try:
            start_day = parse_date(request.data.get("start_day"))
            end_day = parse_date(request.data.get("end_day"))

            passes_per_day = []

            current_date = start_day
            while current_date <= end_day:
                current_date = current_date + timedelta(days=1)
                passes_per_day.append(
                    dict(date=str(current_date), value=PaymentTicket.objects.filter(payment_day=current_date).count())
                )

            return Response({
                "amount_per_day": passes_per_day,
            }, status=status.HTTP_200_OK)

        except (ValueError, TypeError) as e:
            return Response({"error": "Invalid input or format", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminActiveClientsChartData(APIView):
    permission_classes = [IsAuthenticated, isAdmin]

    def post(self, request, *args, **kwargs):
        try:
            start_day = parse_date(request.data.get("start_day"))
            end_day = parse_date(request.data.get("end_day"))

            active_clients = 0
            total_clients = Client.objects.all().count()

            for client in Client.objects.all():
                last_booking_instance = (Booking.objects.filter(client=client).order_by('-date').first())
                if last_booking_instance:
                    last_booking_date = last_booking_instance.date
                    if start_day <= last_booking_date <= end_day:
                        active_clients += 1

            return Response({"chart_data": [
                {"category": "active", "value": active_clients},
                {"category": "non-active", "value": (total_clients - active_clients)},
            ]}, status=status.HTTP_200_OK)

        except (ValueError, TypeError) as e:
            return Response({"error": "Invalid input or format", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminTypeOfServiceChartData(APIView):
    permission_classes = [IsAuthenticated, isAdmin]

    def post(self, request, *args, **kwargs):
        try:
            start_day = parse_date(request.data.get("start_day"))
            end_day = parse_date(request.data.get("end_day"))

            free_climbing = 0
            classes = 0

            current_date = start_day
            while current_date <= end_day:
                current_date = current_date + timedelta(days=1)
                for booking in Booking.objects.filter(date=current_date):
                    if booking.type_of_service == "free_climbing":
                        free_climbing += 1
                    elif booking.type_of_service == "classes":
                        classes += 1

            return Response({"chart_data": [
                {"category": "free climbing", "value": free_climbing},
                {"category": "classes", "value": classes},
            ]}, status=status.HTTP_200_OK)


        except (ValueError, TypeError) as e:
            return Response({"error": "Invalid input or format", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminGetClientData(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsOwnerReadOnlyOrisAdmin]

    def retrieve(self, request, *args, **kwargs):
        user_pk = kwargs.get('pk')  # Get 'pk' from the URL
        user_profile = get_object_or_404(Client, pk=user_pk)

        updateExistingPasses(user_profile)
        serializer = self.get_serializer(user_profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

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


# ADMIN VIEWS FOR SEARCH AND ASSIGN PASSES FOR USERS

class AdminSearchClients(APIView):
    permission_classes = [IsAuthenticated, isAdmin]

    def get(self, request, *args, **kwargs):
        try:
            partial_data = request.query_params.get("input_value")
            clients_found = []

            for client_found in Client.objects.filter(username__icontains=partial_data):
                if client_found not in clients_found:
                    clients_found.append(client_found)

            for client_found in Client.objects.filter(email__startswith=partial_data):
                if client_found not in clients_found:
                    clients_found.append(client_found)

            for client_found in Client.objects.filter(id__contains=partial_data):
                if client_found not in clients_found:
                    clients_found.append(client_found)

            return Response({
                "clients_found": django.core.serializers.serialize('json', clients_found)
            }, status=status.HTTP_200_OK)

        except (ValueError, TypeError) as e:
            return Response({"error": "Invalid input or format", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminGetsTodayPasses(APIView):
    permission_classes = [IsAuthenticated, isAdmin]

    def get(self, request, *args, **kwargs):
        try:
            # partial_data = request.query_params.get("input_value")
            print("TODAYS TIME")
            print(timezone.now().date())
            booking_files = Booking.objects.filter(date=timezone.now().date())

            pprint("booking_files")
            pprint(booking_files)

            serialized_data = BookingSerializer(booking_files, many=True).data

            print("serialized_data")
            pprint(serialized_data)

            return Response({"booking_files": serialized_data}, status=status.HTTP_200_OK)


        except (ValueError, TypeError) as e:
            return Response({"error": "Invalid input or format", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# MERCADO PAGO VIEWS

class MercadoPagoTicket(ModelViewSet):
    queryset = PaymentTicket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        sdk = mercadopago.SDK(os.environ.get('MP_ACCESS_TOKEN'))

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

        sdk = mercadopago.SDK(os.environ.get('MP_ACCESS_TOKEN'))
        merchant_order_id = request.data.get("data", {}).get("id")

        pprint("request.data" + request.data)

        if not merchant_order_id:
            return Response({"error": "No order ID found"}, status=status.HTTP_400_BAD_REQUEST)


        order_data_raw = sdk.merchant_order().get(merchant_order_id)
        order_data = order_data_raw.get("response", {})

        pprint('Merchant Order data \n' + order_data)

        if order_data.get('order_status') == 'paid':
            print(" Ticket paid! $: " + str(order_data.get("paid_amount")))

            try:
                ticket = PaymentTicket.objects.get(order_id=merchant_order_id)
            except PaymentTicket.DoesNotExist:
                return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

            ticket.left_to_pay -= float(order_data.get("paid_amount", 0))

            if ticket.left_to_pay <= 0:
                ticket.left_to_pay = 0
                ticket.status = "in_use"
                ticket.is_expired = False

            ticket.save()

            print("TICKET DATA", ticket)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_202_ACCEPTED)


class MercadoPagoSuccesHookUrlData(APIView):
    permission_classes = [AllowAny]

    def post(self, request, id, topic):

        sdk = mercadopago.SDK(os.environ.get('MP_ACCESS_TOKEN'))
        merchant_order_id = id

        pprint(request.data)

        if not merchant_order_id:
            return Response({"error": "No order ID found"}, status=status.HTTP_400_BAD_REQUEST)

        def get_merchant_order():
            return sdk.merchant_order().get(merchant_order_id)

        def get_ticket(order_id):
            return PaymentTicket.objects.get(order_id=order_id)

        order_data_raw = get_merchant_order()
        order_data = order_data_raw.get("response", {})

        pprint('Merchant Order')
        pprint(order_data)

        if order_data.get('order_status') == 'paid':
            print("Ticket paid!")
            print("$: " + str(order_data.get("paid_amount")))

            try:
                ticket = get_ticket(merchant_order_id)
            except PaymentTicket.DoesNotExist:
                return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

            ticket.left_to_pay -= float(order_data.get("paid_amount", 0))

            if ticket.left_to_pay <= 0:
                ticket.left_to_pay = 0
                ticket.status = "in_use"
                ticket.is_expired = False

            ticket.save()

            print("TICKET DATA", ticket)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_202_ACCEPTED)


class AdminSetPrices(APIView):
    permission_classes = [IsAuthenticated, IsOwnerReadOnlyOrisAdmin]

    def get(self, request, *args, **kwargs):
        # Get all unique types of service
        service_types = MPPassPrice.objects.values_list("type_of_service", flat=True).distinct()

        # Query each type separately and store results in a dictionary
        processed_data = {
            service: list(MPPassPrice.objects.filter(type_of_service=service).values("pass_amount", "price", "id"))
            for service in service_types
        }

        return Response({"processed_data": processed_data}, status=200)

    def post(self, request, *args, **kwargs):
        try:
            price = int(request.data.get('price'))
            pass_amount = int(request.data.get('pass_amount'))
            type_of_service = request.data.get('type_of_service')
            data = dict(price=price, pass_amount=pass_amount, type_of_service=type_of_service)

            serialized_data = MPSerializer(data=data)
            check_valid = serialized_data.is_valid()
            if check_valid:
                serialized_data.save()
                existing_prices = MPPassPrice.objects.all()
                serialize_prices = MPSerializer(existing_prices, many=True)

                return Response({"existing_prices": serialize_prices.data}, status=status.HTTP_200_OK)
            else:
                print(serialized_data.errors)
                return Response({serialized_data.errors}, status=status.HTTP_403_FORBIDDEN)
        except (ValueError, TypeError) as e:
            return Response({"error": "Invalid input or format", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, priceId):
        try:
            print(priceId)
            instance_id = int(priceId)
            object_instance = MPPassPrice.objects.get(id=instance_id)
            object_instance.delete()

            existing_prices = MPPassPrice.objects.all()
            serialize_prices = MPSerializer(existing_prices, many=True)

            return Response({"existing_prices": serialize_prices.data}, status=status.HTTP_200_OK)
        except MPPassPrice.DoesNotExist:
            return Response({"error": "Price not found"}, status=status.HTTP_404_NOT_FOUND)


class AdminShowAllPrices(ModelViewSet):
    queryset = MPPassPrice.objects.all()
    serializer_class = MPSerializer
    permission_classes = [IsAuthenticated, isAdmin]
