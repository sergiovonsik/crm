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
    payment_day = models.DateField(default=timezone.now, editable=False)

    amount_of_uses = models.IntegerField(default=0)

    amount_of_uses_LEFT = models.IntegerField(default=0)

    owner = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        unique=False,
        related_name='payment_ticket',
    )

    order_id = models.CharField(max_length=100, default="Null", blank=False)

    expire_time = models.DateField(default=get_default_date_30_days, editable=False, blank=True, null=True)

    is_expired = models.BooleanField(default=False)

    status = models.CharField(
        max_length=30,
        choices=[('expired', 'expired'), ('in_use', 'in_use'), ('unpaid', 'unpaid')],
        default='unpaid',
        editable=True,
    )

    price = models.IntegerField(default=0)

    left_to_pay = models.IntegerField(default=0)

    def __str__(self):
        return (f"Ticket N~{self.pk}, {self.owner.username} \n"
                f"Paid for {self.type_of_service} on {self.payment_day}\n"
                f"Amount of uses left: {self.amount_of_uses_LEFT}\n"
                f"Ticket Expired Status: {self.is_expired}")
