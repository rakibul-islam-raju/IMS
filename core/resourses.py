from import_export import resources
from import_export.fields import Field
from .models import SellProduct


class SellProductResource(resources.ModelResource):
    product = Field(attribute='product_name', column_name='product_name')
    quantity = Field(attribute='quantity', column_name='quantity')
    price = Field(attribute='sell_price', column_name='price')
    total_amount = Field(attribute='get_total_amount', column_name='total_amount')
    paid_amount = Field(attribute='paid_amount', column_name='paid_amount')
    due_amount = Field(attribute='get_due_amount', column_name='due_amount')
    customer_name = Field(attribute='customer_name', column_name='customer_name')
    customer_phone = Field(attribute='customer_phone', column_name='customer_phone')
    description = Field(attribute='description', column_name='description')
    date = Field(attribute='date_added', column_name='date')

    class Meta:
        model = SellProduct
