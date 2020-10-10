from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import (View,
                                TemplateView,
                                ListView,
                                CreateView,
                                DetailView,
                                UpdateView,
                                DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import *
from .forms import *
from .filters import *


class SellProductFilterView(LoginRequiredMixin,
                        UserPassesTestMixin,
                        SuccessMessageMixin,
                        View):

    def get(self, request, *args, **kwargs):
        f = SellProductFilter(self.request.GET, queryset=SellProduct.objects.all())
        context = {
            'filter': f,
            'title': 'Sell Report'
        }
        return render(self.request, 'sell_filter.html', context)
    
    def test_func(self, *args, **kwargs):
        if self.request.user.is_staff:
            return True
        return False


class HomeView(LoginRequiredMixin,
            TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stocks"] = Stock.objects.filter(is_active=True)
        context["sells"] = SellProduct.objects.filter(is_active=True)
        return context


class UserManagement(LoginRequiredMixin,
                    UserPassesTestMixin,
                    View):
    def get(self, *args, **kwargs):
        users = User.objects.all()
        context = {
            'users': users,
            'title': 'User Management',
        }
        return render(self.request, 'users.html', context)
    
    def test_func(self, *args, **kwargs):
        if self.request.user.is_staff:
            return True
        return False


class EditUserManagent(LoginRequiredMixin,
                    UserPassesTestMixin,
                    SuccessMessageMixin,
                    UpdateView):
    model = User
    form_class = UserPermissionForm
    template_name = 'edit-user.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    success_url = 'user'
    success_message = "Changes saved successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit User'
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)
    
    def test_func(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return True
        return False


class PurchaseProductCreateView(LoginRequiredMixin,
                                UserPassesTestMixin,
                                SuccessMessageMixin,
                                CreateView):
    model = PurchaseProduct
    form_class = PurchaseCreateForm
    template_name = 'purchase.html'
    success_url = 'purchase'
    success_message = "%(product_name)s was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Purchase'
        context["purchases"] = PurchaseProduct.objects.filter(is_active=True)
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.save()
        return super(PurchaseProductCreateView, self).form_valid(form)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class StockCreateView(LoginRequiredMixin,
                    UserPassesTestMixin,
                    SuccessMessageMixin,
                    CreateView):
    model = Stock
    form_class = StockCreateForm
    template_name = 'stock.html'
    success_url = 'stock'
    success_message = "%(product_name)s was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Stock'
        context["stocks"] = Stock.objects.filter(is_active=True)
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.save()
        return super(StockCreateView, self).form_valid(form)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class SellProductCreateView(LoginRequiredMixin,
                        UserPassesTestMixin,
                        SuccessMessageMixin,
                        CreateView):
    model = SellProduct
    form_class = SellProductCreateForm
    template_name = 'sell.html'
    success_url = 'sell'
    success_message = "%(product_name)s was created successfully"

    def post(self, *args, **kwargs):
        form = SellProductCreateForm(self.request.POST or None)

        if form.is_valid():
            product_name = form.cleaned_data.get('product_name')
            print(f'product: {product_name}')
            product_instance = get_object_or_404(Stock, product_name=product_name)
            quantity = form.cleaned_data.get('quantity')

            if quantity <= product_instance.quantity:
                sell = form.save(commit=False)
                sell.added_by = self.request.user
                sell.save()

                new_qntty = product_instance.quantity - quantity
                product_instance.quantity = new_qntty
                product_instance.save(update_fields=['quantity'])
            else:
                messages.warning(self.request, 'Invalid Qunatity')
                return redirect('sell')
        messages.success(self.request, f'{product_instance.product_name} was created successfully')        
        return redirect('sell')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Sell'
        context["sells"] = SellProduct.objects.filter(is_active=True)
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.save()
        return super(SellProductCreateView, self).form_valid(form)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class SellProductByID(LoginRequiredMixin,
                        UserPassesTestMixin,
                        SuccessMessageMixin,
                        View):

    def get(self, *args, **kwargs):
        product_instance = get_object_or_404(Stock, pk=self.kwargs['pk'])
        form = SellProductCreateForm(instance=product_instance, initial={
            'product_name': product_instance
        })
        context = {
            'form': form,
            'title': 'New Sell',
            'sells': SellProduct.objects.all()
        }
        return render(self.request, 'sell.html', context)

    def post(self, *args, **kwargs):
        product_instance = get_object_or_404(Stock, pk=self.kwargs['pk'])
        form = SellProductCreateForm(self.request.POST or None)
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')

            if quantity <= product_instance.quantity:
                sell = form.save(commit=False)
                sell.added_by = self.request.user
                sell.save()

                new_qntty = product_instance.quantity - quantity
                product_instance.quantity = new_qntty
                product_instance.save(update_fields=['quantity'])
            else:
                messages.warning(self.request, 'Invalid Qunatity')
                return redirect('sell')
        messages.success(self.request, f'{product_instance.product_name} was created successfully')        
        return redirect('sell')

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.save()
        return super(SellProductByID, self).form_valid(form)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


# ============ update view ===========

class PurchaseProductUpdateView(LoginRequiredMixin,
                                UserPassesTestMixin,
                                SuccessMessageMixin,
                                UpdateView):
    model = PurchaseProduct
    form_class = PurchaseCreateForm
    template_name = 'purchase.html'
    success_url = 'purchase'
    success_message = "%(product_name)s was updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Purchase'
        context["purchases"] = PurchaseProduct.objects.filter(is_active=True)
        return context
    
    def get_success_url(self, **kwargs):
        return reverse(self.success_url)
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class StockUpdateView(LoginRequiredMixin,
                    UserPassesTestMixin,
                    SuccessMessageMixin,
                    UpdateView):
    model = Stock
    form_class = StockCreateForm
    template_name = 'stock.html'
    success_url = 'stock'
    success_message = "%(product_name)s was updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Stock'
        context["stocks"] = Stock.objects.filter(is_active=True)
        return context
    
    def get_success_url(self, **kwargs):
        return reverse(self.success_url)
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class SellProductUpdateView(LoginRequiredMixin,
                            UserPassesTestMixin,
                            SuccessMessageMixin,
                            UpdateView):
    model = SellProduct
    form_class = SellProductCreateForm
    template_name = 'sell.html'
    success_url = 'sell'
    success_message = "%(product_name)s was updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Sell'
        context["sells"] = SellProduct.objects.filter(is_active=True)
        return context
    
    def get_success_url(self, **kwargs):
        return reverse(self.success_url)
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


# ========== delete views ==============

class PurchaseProductDeleteView(LoginRequiredMixin,
                                UserPassesTestMixin,
                                SuccessMessageMixin,
                                DeleteView):
    model = PurchaseProduct
    template_name = 'purchase.html'
    success_url = 'purchase'
    success_message = "%(name)s was deleted successfully"

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class StockDeleteView(LoginRequiredMixin,
                    UserPassesTestMixin,
                    SuccessMessageMixin,
                    DeleteView):
    model = Stock
    template_name = 'stock.html'
    success_url = 'stock'
    success_message = "%(name)s was deleted successfully"

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class SellProductDeleteView(LoginRequiredMixin,
                            UserPassesTestMixin,
                            SuccessMessageMixin,
                            DeleteView):
    model = SellProduct
    template_name = 'sell.html'
    success_url = 'sell'
    success_message = "%(name)s was deleted successfully"

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
