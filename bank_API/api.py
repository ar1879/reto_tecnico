from .models import Account, Transaction
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import  AccountSerializer, TransactionSerializer


class AccountViewSet(viewsets.ModelViewSet):
    # pagination_class = PageNumberPagination
    # page_size = 25  # Establece el tamaño de la página en 20
    queryset = Account.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AccountSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.queryset
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()
    
    def list(self, request):
        data = self.queryset
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
            query = self.get_queryset(pk)
            if query:
                query_serializer = AccountSerializer(query)
                return Response(query_serializer.data, status=status.HTTP_200_OK)
            return Response({'error':'No existe ninguna cuenta con este id!'}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request):
        # send information to serializer 
        serializer = self.serializer_class(data=request.data)     
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Cuenta creada correctamente!'}, status=status.HTTP_201_CREATED)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            # send information to serializer referencing the instance
            query_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)            
            if query_serializer.is_valid():
                query_serializer.save()
                return Response({'message':'Cuenta actualizada correctamente!'}, status=status.HTTP_200_OK)
            return Response({'message':'', 'error':query_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, pk=None):
        query = self.get_queryset().filter(id=pk).first() # get instance        
        if query:
            query.delete()
            query.save()
            return Response({'message':'Cuenta eliminada correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe ninguna cuenta con este id!'}, status=status.HTTP_400_BAD_REQUEST)
    

class TransactionViewSet(viewsets.ModelViewSet):
    # pagination_class = PageNumberPagination
    # page_size = 25  # Establece el tamaño de la página en 20
    queryset = Transaction.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TransactionSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.queryset
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()
    
    def list(self, request):
        data = self.queryset
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
            query = self.get_queryset(pk)
            if query:
                query_serializer = TransactionSerializer(query)
                return Response(query_serializer.data, status=status.HTTP_200_OK)
            return Response({'error':'No existe ninguna Transaccion con este id!'}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request):
        check_initial = Transaction.objects.filter(account_number=request.data['account_number'])
        # if len(check_initial) != 0:
            # check_initial.
        
        serializer = self.serializer_class(data=request.data) 
        account = Account.objects.filter(id=request.data['account_number'])
        print(account)
        if account.exists():  
            if serializer.is_valid():
                account = account.first()
                transaction = serializer.save()
                if serializer.data['transaction_type'] == 'deposit':
                    account.balance += transaction.amount
                elif serializer.data['transaction_type'] == 'withdrawal':
                    account.balance -= transaction.amount
                    
                account.save()
                return Response({'message': 'Transaccion creada correctamente!'}, status=status.HTTP_201_CREATED)
            return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            
            return Response({'message':'La cuenta seleccionada para la transaccion no existe'}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        if self.get_queryset(pk):
            a = self.get_queryset(pk)
            
            # send information to serializer referencing the instance
            query_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)            
            if query_serializer.is_valid():
                query_serializer.save()
                account = Account.objects.filter(id=request.data['account_number']).first()
                if query_serializer.data['transaction_type'] == 'deposit':
                    account.balance -= a.amount
                    account.balance += float(request.data['amount'])
                elif query_serializer.data['transaction_type'] == 'withdrawal':
                    account.balance += a.amount
                    account.balance -= float(request.data['amount'])

                account.save()
                return Response({'message':'Transaccion actualizada correctamente!', 'data':query_serializer.data}, status=status.HTTP_200_OK)
            return Response({'message':'', 'error':query_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, pk=None):
        query = self.get_queryset().filter(id=pk).first() # get instance        
        if query:
            query.delete()
            query.save()
            return Response({'message':'Transaccion eliminada correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe ninguna transaccion con este id!'}, status=status.HTTP_400_BAD_REQUEST)
    


