from rest_framework.routers import DefaultRouter
from wallet.views import WalletViewSet

router = DefaultRouter()

router.register("wallet", WalletViewSet)

urlpatterns = router.urls
