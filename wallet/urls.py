from rest_framework.routers import DefaultRouter
from wallet.views import WalletViewSet, TransactionViewSet

router = DefaultRouter()

router.register("wallet", WalletViewSet)
router.register("transaction", TransactionViewSet)

urlpatterns = router.urls
