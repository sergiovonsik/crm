from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
from django.utils import timezone


def get_default_date_30_days():
    # Get current date and add 30 days
    return (timezone.now() + timedelta(days=30)).date()


class Client(AbstractUser):
    google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return f" pk:{self.pk}: {self.username}"


class PaymentTicket(models.Model):
    type_of_service = models.CharField(
        max_length=30,
        choices=[('classes', 'classes'), ('free_climbing', 'free_climbing')],
    )
    payment_day = models.DateField(auto_now_add=True, editable=False)

    amount_of_uses = models.IntegerField(default=0)

    amount_of_uses_LEFT = models.IntegerField(default=0)

    owner = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        unique=False,
        related_name='payment_ticket',
    )

    order_id = models.CharField(max_length=100, default="Null", blank=False)

    expire_time = models.DateField(default=get_default_date_30_days, blank=False, null=False )

    is_expired = models.BooleanField(default=False, editable=True)

    status = models.CharField(
        max_length=30,
        choices=[('expired', 'expired'), ('in_use', 'in_use'), ('unpaid', 'unpaid')],
        default='unpaid',
        editable=True,
    )

    price = models.IntegerField(default=0)

    left_to_pay = models.IntegerField(default=0)

    def __str__(self):
        return (f"Ticket #{self.pk} | Owner: {self.owner.username} | Service: {self.type_of_service} | \n"
                f"Payment Day: {self.payment_day} | Expires: {self.expire_time} | \n"
                f"Uses Left: {self.amount_of_uses_LEFT} | Expired: {self.is_expired} | \n"
                f"Status: {self.status} | Price: {self.price} | Left to Pay: {self.left_to_pay} \n")


class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings')
    ticket = models.ForeignKey(PaymentTicket, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    type_of_service = models.CharField(
        max_length=30,
        choices=[('classes', 'classes'), ('free_climbing', 'free_climbing')],
    )
    hour = models.CharField(
        max_length=30,
        choices=[('6 to 8', '6 to 8'), ('8 to 10', '8 to 10'), ("", "")],
        default="",
        blank=True,
        null=True,
    )

    def __str__(self):
        return (f"Booking #{self.pk} | Client: {self.client.username} | Ticket: {self.ticket.pk} | \n"
                f"Date: {self.date} | Created At: {self.created_at} | \n"
                f"Activity Type: {self.type_of_service} | Hours: {self.hour}")

    class Meta:
        unique_together = ('client', 'date')  # Prevent duplicate bookings per day


class MPPassPrice(models.Model):
    pass_amount = models.IntegerField()
    price = models.IntegerField()
    type_of_service = models.CharField(
        max_length=30,
        choices=[('classes', 'classes'), ('free_climbing', 'free_climbing')],
    )

    def __str__(self):
        return (f"Booking #{self.pk} | Price: {self.price} | Amount: {self.pass_amount} | \n"
                f"Activity Type: {self.type_of_service} |")

    class Meta:
        unique_together = ('pass_amount', 'type_of_service')  # Prevent duplicate bookings per day
