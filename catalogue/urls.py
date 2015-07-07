from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'offers', views.OfferViewSet)
router.register(r'skus', views.SKUViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'tariffplans', views.TariffPlanViewSet)
router.register(r'promotions', views.PromotionViewSet)