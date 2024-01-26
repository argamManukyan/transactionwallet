from rest_framework import serializers

from wallet.models import Wallet, Transaction


class TransactionModelSerializer(serializers.ModelSerializer):
    """Serializer for create/update/read transaction data"""

    class Meta:
        model = Transaction
        fields = ["id", "wallet", "txid", "amount"]


class WalletModelSerializer(serializers.ModelSerializer):
    """Serializer for create/update/read wallet data"""

    transactions = TransactionModelSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = ["id", "balance", "label", "transactions"]
        read_only_fields = ["balance"]
