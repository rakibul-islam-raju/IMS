from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django_filters.views import FilterView

from core.models import SellProduct
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('', HomeView.as_view(), name='home'),
    path('users/', UserManagement.as_view(), name='user'),
    path('user/<username>/', EditUserManagent.as_view(), name='user-edit'),

    path('sell/filter/', SellProductFilterView.as_view(), name='sell-filter'),
    path('sells/filter/', FilterView.as_view(model=SellProduct, template_name='sell_filter'), name='sell-filter'),

    path('purchases/', PurchaseProductCreateView.as_view(), name='purchase'),
    path('purchase/<int:pk>/', PurchaseProductUpdateView.as_view(), name='purchase-update'),
    path('purchase/delete/<int:pk>/', PurchaseProductDeleteView.as_view(), name='purchase-delete'),

    path('stocks/', StockCreateView.as_view(), name='stock'),
    path('stocks/<int:pk>/', StockUpdateView.as_view(), name='stock-update'),
    path('stocks/delete/<int:pk>/', StockDeleteView.as_view(), name='stock-delete'),

    path('sells/', SellProductCreateView.as_view(), name='sell'),
    path('sells/<int:pk>/', SellProductUpdateView.as_view(), name='sell-update'),
    path('sells/product/<int:pk>/', SellProductByID.as_view(), name='sell-product-by-id'),
    path('sells/delete/<int:pk>/', SellProductDeleteView.as_view(), name='sell-delete'),
]

admin.site.site_header = 'Inventory Admin Panel'
admin.site.index_title = 'Inventory management'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
