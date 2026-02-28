from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ItemViewSet, StoreViewSet, StoreItemViewSet, StockTransferViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('items', ItemViewSet, basename='item')
router.register('stores', StoreViewSet, basename='store')
router.register('store-items', StoreItemViewSet, basename='storeitem')
router.register('stock-transfers', StockTransferViewSet, basename='stocktransfer')

urlpatterns = [
    path('', include(router.urls)),
]
