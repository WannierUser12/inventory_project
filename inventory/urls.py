from django.urls import include, path

from core.router import CustomDefaultRouter
from . import views

router = CustomDefaultRouter(base_prefix="inventorys")
router_ = CustomDefaultRouter(base_prefix="arrival")
router__ = CustomDefaultRouter(base_prefix="shipping")
router___ = CustomDefaultRouter(base_prefix="import_products")
router____ = CustomDefaultRouter(base_prefix="import_products_shipment")
router_____ = CustomDefaultRouter(base_prefix="import_products_managers")

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

router___.register(
    "",
    views.ImportproductsViewSet,
    basename="import_products",
)

router_____.register(
    "",
    views.ImportproductsViewSet,
    basename="import_products_managers",
)

router____.register(
    "",
    views.ImportproductsShipmentViewSet,
    basename="import_products_shipment",
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
    path("", include(router___.urls)),
    path("", include(router____.urls)),
    path("", include(router_____.urls)),
]
