from django.db import models
from django.utils import timezone

# Create your models here.
class Account(models.Model):
    TYPE_CHOICES = (
        ('savings', 'savings'),
        ('checking', 'checking'),
    )

    account_number = models.CharField(max_length=10, blank=False, null=False, unique=True)
    balance = models.FloatField(default=0)
    customer_name = models.CharField(max_length=100, blank=False, null=False)
    account_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    last_updated = models.DateTimeField('Ultima actualización', auto_now=True)

    # def __int__(self) -> int:
    #     return self.account_number

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'deposit'),
        ('withdrawal', 'withdrawal'),
    )
    
    # transaction_id = models.AutoField(primary_key=True)
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    timestamp = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=100, default='Initial Deposit')
    status = models.BooleanField(max_length=7, default=True)
