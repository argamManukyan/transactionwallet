from rest_framework.viewsets import ModelViewSet

from wallet.serializers import WalletModelSerializer
from wallet.services import WalletService


class WalletViewSet(ModelViewSet):
    queryset = WalletService.get_wallets_list()
    serializer_class = WalletModelSerializer
    lookup_field = "id"
    http_method_names = ["post", "patch", "delete", "get"]
