from django.db.models import QuerySet

from wallet.models import Wallet


class WalletService:
    model = Wallet

    @classmethod
    def get_wallets_list(cls) -> QuerySet[model]:
        """Returns wallets sequence"""
        return cls.model.objects.all()
