from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from apps.wallet.filters import TransactionFilter, WalletFilter
from apps.wallet.models import Transaction, Wallet
from apps.wallet.pagination import TransactionPagination, WalletPagination
from apps.wallet.serializers import TransactionSerializer, WalletSerializer


class WalletListCreateView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['id', 'label', 'balance']
    pagination_class = WalletPagination
    filterset_class = WalletFilter


class WalletRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['txid', 'amount', 'created_at']
    pagination_class = TransactionPagination
    filterset_class = TransactionFilter


class TransactionRetrieveUpdateDestroyView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
