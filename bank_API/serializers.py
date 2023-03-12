from rest_framework import serializers
from .models import Account
from .models import Transaction



class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 
                  'account_number',
                  'balance',
                  'customer_name',
                  'account_type',
                  'created_at',
                  'last_updated',
                  )
        read_only_fields = ('balance',)


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 
                  'account_number',
                  'amount',
                  'timestamp',
                  'transaction_type',
                  'description',
                  'status',
                  )
        read_only_fields = ('status',)
        
