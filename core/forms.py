from django import forms
from .models import *
from allauth.account.forms import SignupForm

offices = Office.objects.all()

class MyCustomSignupForm(SignupForm):
    office = forms.ModelChoiceField(offices)

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        office = self.cleaned_data['office']
        user.office = office
        user.save()
        return user


class HelpcenterForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': '3'}))


class UserPermissionForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username',
                'email',
                'first_name',
                'last_name',
                'is_active',
                'is_staff',]


class PurchaseCreateForm(forms.ModelForm):

    class Meta:
        model = PurchaseProduct
        fields = ['product_name',
                'price',
                'quantity',
                'description']
        labels = {
            'product_name': 'Product (পণ্য)',
            'price': 'Price (মূল্য)',
            'quantity': 'Quantity (পরিমাণ)',
            'description': 'Description (বর্ণনা)'
        }
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'price': forms.TextInput(attrs={'placeholder': 'Taka'}),
            'quantity': forms.TextInput(attrs={'placeholder': 'kg'}),
            'description': forms.Textarea(attrs={'rows': '2'}),
        }    


class StockCreateForm(forms.ModelForm):

    class Meta:
        model = Stock
        fields = ['product_name',
                'sell_price',
                'quantity',
                'description']
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'sell_price': forms.TextInput(attrs={'placeholder': 'Taka'}),
            'quantity': forms.TextInput(attrs={'placeholder': 'kg'}),
            'description': forms.Textarea(attrs={'rows': '2'}),
        }
        labels = {
                'product_name': 'Product (পণ্য)',
                'quantity': 'Quantity (পরিমাণ)',
                'sell_price': 'Sell Price (বিক্রয় মূল্য)',
                'description': 'Description (বর্ণনা)',
        } 


class SellProductCreateForm(forms.ModelForm):

    class Meta:
        model = SellProduct
        fields = ['product_name',
                'quantity',
                'sell_price',
                'customer_name',
                'customer_phone',
                'paid_amount',
                'description']
        labels = {
                'product_name': 'Product (পণ্য)',
                'quantity': 'Quantity (পরিমাণ)',
                'sell_price': 'Sell Price (বিক্রয় মূল্য)',
                'customer_name': 'Customer Name (ক্রেতার নাম)',
                'customer_phone': 'Customer Phone (ক্রেতার নাম্বার)',
                'paid_amount': 'Paid Amount (পরিশোধিত টাকা)',
                'description': 'Description (বর্ণনা)',
        }
        widgets = {
            'sell_price': forms.TextInput(attrs={'placeholder': 'Taka'}),
            'paid_amount': forms.TextInput(attrs={'placeholder': 'Taka'}),
            'customer_name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'customer_phone': forms.TextInput(attrs={'placeholder': 'Phone'}),
            'quantity': forms.TextInput(attrs={'placeholder': 'kg'}),
            'paid_amount': forms.TextInput(attrs={'placeholder': 'Taka'}),
            'description': forms.Textarea(attrs={'rows': '2'}),
        }
