from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from wallet.serializers import WalletModelSerializer, TransactionModelSerializer
from wallet.services import WalletService, TransactionService


class WalletViewSet(ModelViewSet):
    """View for Wallet CRUD"""

    queryset = WalletService.get_wallets_list()
    serializer_class = WalletModelSerializer
    lookup_field = "id"
    http_method_names = ["post", "patch", "delete", "get"]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ["label", "balance"]
    search_fields = ["label"]


class TransactionViewSet(ModelViewSet):
    """View for Transaction create and delete"""

    serializer_class = TransactionModelSerializer
    queryset = TransactionService.get_transactions_list()
    lookup_field = "id"
    http_method_names = ["post", "delete", "get"]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ["amount", "txid", "wallet_id"]
    search_fields = [
        "amount",
        "txid",
    ]

    def perform_create(self, serializer):
        data = serializer.save()

        # Updating wallet balance
        WalletService.update_wallet_amount(wallet_id=data.wallet_id, amount=data.amount)
