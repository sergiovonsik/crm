from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
#----
from datetime import timedelta
from django.utils import timezone

def get_default_date_30_days():
    # Get current date and add 30 days
    return timezone.now().date() + timedelta(days=30)

class Client(AbstractUser):
    free_climbing_left = models.IntegerField(default=0)
    classes_left = models.IntegerField(default=0)

    def __str__(self):
        return f" pk:{self.pk}: {self.username} has {self.classes_left}:classes {self.free_climbing_left}: free_passes "



class PaymentTicket(models.Model):
    type_of_service = models.CharField(
        max_length=30,
        choices=[('classes', 'CLASS'), ('free_climbing', 'FREE_CLIMBING')],
    )
    payment_day = models.DateField(default=timezone.now, editable=False)

    amount_of_uses = models.IntegerField(default=0)

    owner = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        unique=False,
        related_name='payment_ticket',
        blank=True,
        null=True
    )

    expire_time = models.DateField(default=get_default_date_30_days, editable=False, blank=True, null=True)

    is_expired = models.BooleanField(default=False)


    def __str__(self):
        return f"Ticket N~{self.pk}, {self.owner.username} paid for {self.type_of_service} on {self.payment_day}"
