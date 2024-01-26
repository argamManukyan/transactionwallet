from decimal import Decimal

from django.db.models import QuerySet
from rest_framework.exceptions import NotFound

from wallet.models import Wallet, Transaction


class WalletService:
    model = Wallet

    @classmethod
    def get_wallets_list(cls) -> QuerySet[model]:
        """Returns wallets sequence"""
        return cls.model.objects.all()

    @classmethod
    def get_wallet_by_id(cls, wallet_id: int) -> model:
        """Returns a wallet instance if founds any wallet by the given id"""
        wallet = cls.model.objects.filter(id=wallet_id).first()

        if not wallet:
            raise NotFound

        return wallet

    @classmethod
    def update_wallet_amount(cls, wallet_id: int, amount: Decimal):
        """Updates wallet balance"""

        wallet = cls.get_wallet_by_id(wallet_id=wallet_id)
        wallet.balance += amount
        wallet.save(update_fields=["balance"])


class TransactionService:

    model = Transaction

    @classmethod
    def get_transactions_list(cls):
        return cls.model.objects.all()
