from rest_framework import serializers

from core.exceptions import NotEnoughFunds
from wallet.services import WalletService
from wallet.models import Wallet, Transaction


class TransactionModelSerializer(serializers.ModelSerializer):
    """Serializer for create/update/read transaction data"""

    class Meta:
        model = Transaction
        fields = ["id", "wallet", "txid", "amount"]

    def validate(self, attrs):
        amount = attrs["amount"]
        wallet = WalletService.get_wallet_by_id(wallet_id=attrs["wallet"].id)

        if amount < 0 and wallet.balance + amount < 0:
            raise NotEnoughFunds

        return super().validate(attrs)


class WalletModelSerializer(serializers.ModelSerializer):
    """Serializer for create/update/read wallet data"""

    transactions = TransactionModelSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = ["id", "balance", "label", "transactions"]
        read_only_fields = ["balance"]
