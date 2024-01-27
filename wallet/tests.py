import os
from decimal import Decimal

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.test import APITestCase

from core.exceptions import NotEnoughFunds
from wallet.services import WalletService

WALLET_URL_PATH = "/api/v1/wallet"
TRANSACTION_URL_PATH = "/api/v1/transaction"


class TestWallet(APITestCase):

    def test_create_wallet(self):
        data = {"label": "My Wallet"}
        result = self.client.post(WALLET_URL_PATH, data, format="json")
        assert result.data["label"] == data["label"]
        assert result.status_code == status.HTTP_201_CREATED

    def test_get_wallet(self):
        wallet_id = 1
        data = {"label": "My Wallet"}
        self.client.post(WALLET_URL_PATH, data, format="json")
        result = self.client.get(f"{WALLET_URL_PATH}/{wallet_id}", format="json")

        assert result.status_code == status.HTTP_200_OK
        assert result.data["label"] == "My Wallet"
        assert result.data["transactions"] == []

    def test_get_wallet_fail(self):
        wallet_id = 1
        result = self.client.get(f"{WALLET_URL_PATH}/{wallet_id}", format="json")
        assert result.status_code == status.HTTP_404_NOT_FOUND

    def test_get_wallet_list(self):
        data = {"label": "My Wallet"}
        self.client.post(WALLET_URL_PATH, data, format="json")
        result = self.client.get(WALLET_URL_PATH, format="json")
        assert result.status_code == status.HTTP_200_OK
        assert result.data[0]["label"] == "My Wallet"
        assert result.data[0]["transactions"] == []

    def test_patch_wallet(self):
        wallet_id = 1
        data = {"label": "My Wallet"}
        self.client.post(WALLET_URL_PATH, data, format="json")

        result = self.client.patch(
            f"{WALLET_URL_PATH}/{wallet_id}",
            data={"label": "New Wallet"},
            format="json",
        )

        assert result.data["label"] != data["label"]
        assert result.status_code == status.HTTP_200_OK

    def test_delete_wallet(self):
        data = {"label": "My Wallet"}
        wallet_id = 1
        self.client.post(WALLET_URL_PATH, data, format="json")
        result = self.client.delete(f"{WALLET_URL_PATH}/{wallet_id}")
        assert result.status_code == status.HTTP_204_NO_CONTENT

    def test_raise_not_found(self):
        try:
            WalletService.get_wallet_by_id(wallet_id=23)
        except NotFound as e:
            assert e.status_code == status.HTTP_404_NOT_FOUND


class TestTransaction(APITestCase):

    def setUp(self):
        data = {"label": "My Wallet"}
        self.client.post(WALLET_URL_PATH, data, format="json")

    def test_create_transaction(self):
        data = {"wallet": 1, "txid": "xasxasx", "amount": "300.1"}

        result = self.client.post(TRANSACTION_URL_PATH, data, format="json")
        wallet = WalletService.get_wallet_by_id(wallet_id=1)
        assert result.status_code == status.HTTP_201_CREATED
        assert result.data["txid"] == data["txid"]
        assert f"{wallet.balance}" == result.data["amount"]

    def test_create_transaction_taxid_fail(self):
        data_one = {"wallet": 1, "txid": "xasxasx", "amount": "300.1"}
        data_two = {"wallet": 1, "txid": "xasxasx", "amount": "300.1"}

        self.client.post(TRANSACTION_URL_PATH, data_one, format="json")

        response = self.client.post(TRANSACTION_URL_PATH, data_two, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_transaction_funds_fail(self):
        data_one = {"wallet": 1, "txid": "xasxasx", "amount": "-300.1"}

        self.client.post(TRANSACTION_URL_PATH, data_one, format="json")

        response = self.client.post(TRANSACTION_URL_PATH, data_one, format="json")
        assert response.data["errors"]["detail"] == NotEnoughFunds.default_detail
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_transaction(self):
        data_one = {"wallet": 1, "txid": "xasxasx", "amount": "300.1"}

        self.client.post(TRANSACTION_URL_PATH, data_one, format="json")

        result = self.client.get(f"{TRANSACTION_URL_PATH}/1")
        assert result.data["amount"] == data_one["amount"]
        assert result.data["txid"] == data_one["txid"]

    def test_get_transaction_fail(self):
        data_one = {"wallet": 1, "txid": "xasxasx", "amount": "300.1"}

        self.client.post(TRANSACTION_URL_PATH, data_one, format="json")

        result = self.client.get(f"{TRANSACTION_URL_PATH}/2")
        assert result.status_code == status.HTTP_404_NOT_FOUND

    def test_get_transaction_list(self):
        data_one = {"wallet": 1, "txid": "xasxasx", "amount": "300.1"}
        data_two = {"wallet": 1, "txid": "xasxaxsx", "amount": "400.1"}

        res1 = self.client.post(TRANSACTION_URL_PATH, data_one, format="json")
        res2 = self.client.post(TRANSACTION_URL_PATH, data_two, format="json")

        result = self.client.get(TRANSACTION_URL_PATH, format="json")
        wallet = WalletService.get_wallet_by_id(wallet_id=1)
        total_balance = Decimal(res1.data["amount"]) + Decimal(res2.data["amount"])

        assert wallet.balance == total_balance
        assert len(result.data) == 2
