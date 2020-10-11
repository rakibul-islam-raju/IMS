import django_filters
from .models import *

class SellProductFilter(django_filters.FilterSet):

    class Meta:
        model = SellProduct
        
        fields = {
            'product_name': ['exact'],
            'customer_name': ['exact'],
            'customer_phone': ['exact'],
            'date_added': ['exact', 'gt', 'lt'],
        }
