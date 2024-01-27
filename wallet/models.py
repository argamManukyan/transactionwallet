from django.db import models

from wallet.helpers import BaseModel


class Wallet(BaseModel):
    """Wallet model"""

    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=18, decimal_places=1, default=0)

    def __str__(self):
        return f"{self.label} - {self.balance}"


class Transaction(BaseModel):
    """Transactions save model"""

    txid = models.CharField(unique=True, db_index=True, max_length=255)
    amount = models.DecimalField(max_digits=18, decimal_places=1)
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        related_name="transactions",
    )  # permitted to delete wallet till transactions are

    def __str__(self):
        return f"{self.wallet.id} - {self.amount} -> {self.txid}"
