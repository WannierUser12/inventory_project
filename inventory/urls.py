from django.urls import include, path

from core.router import CustomDefaultRouter
from . import views

router = CustomDefaultRouter(base_prefix="inventorys")
router_ = CustomDefaultRouter(base_prefix="arrival")
router__ = CustomDefaultRouter(base_prefix="shipping")

router.register(
    "",
    views.InventoryViewSet,
    basename="inventory",
)
router.register(
    "products",
    views.ProductViewSet,
    basename="products",
)
router_.register(
    "",
    views.ArrivalMixinView,
    basename="arrival",
)

router__.register(
    "",
    views.ShippingMixinView,
    basename="shipping",
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(router_.urls)),
    path("", include(router__.urls)),
]
