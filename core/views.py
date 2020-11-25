from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
from django.views.generic import (View,
                                TemplateView,
                                ListView,
                                CreateView,
                                DetailView,
                                UpdateView,
                                DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Sum
import json
from datetime import date
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import *
from .forms import *
from .filters import *
from .resourses import *


class ChartView(TemplateView,
                LoginRequiredMixin,
                UserPassesTestMixin):
    template_name = 'charts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stocks"] = Stock.objects.filter(is_active=True)
        context["sells"] = SellProduct.objects.filter(is_active=True)
        context["purchases"] = PurchaseProduct.objects.filter(is_active=True)
        return context
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


@login_required()
def sell_invoice(request, *args, **kwargs):
    pk = kwargs.get('pk')
    sell = get_object_or_404(SellProduct, pk=pk)

    template_path = 'sell-invoice.html'
    context = {'sell': sell}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if we want to download the pdf :
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if we want to display the pdf :
    filename = f'invoice-{pk}-{date.today()}'
    response['Content-Disposition'] = f'filename="{filename}.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required()
def get_help(request):
    if request.method == 'POST':
        form = HelpcenterForm(request.POST or None)
        if form.is_valid():
            # name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            recipients = ['rakibul.islam7772588@gmail.com']

            # final_message = f''

            send_mail(subject, message, email, recipients)
            messages.success(request, 'Email successfully sent.')
        else:
            messages.warning(request, 'Something went wrong. Please try again.')
    form = HelpcenterForm()

    context = {
        'title': 'Help Center',
        'form': form
    }
    return render(request, 'help.html', context)

@login_required()
def download_sells_csv(request):
    sells_resource = SellProductResource()
    dataset = sells_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sells.csv"'
    return response


class SellProductReportView(LoginRequiredMixin,
                        UserPassesTestMixin,
                        SuccessMessageMixin,
                        View):

    def get(self, request, *args, **kwargs):
        queryset = SellProduct.objects.filter(is_active=True)
        f = SellProductFilter(self.request.GET, queryset)

        total_sell = sum([item.get_total_amount for item in f.qs])
        total_paid = sum([item.paid_amount for item in f.qs])
        total_due = sum([item.get_due_amount for item in f.qs])

        context = {
            'filter': f,
            'total_sell': total_sell,
            'total_paid': total_paid,
            'total_due': total_due,
            'title': 'Sell Report'
        }
        return render(self.request, 'sell_report.html', context)
    
    def test_func(self, *args, **kwargs):
        if self.request.user.is_staff:
            return True
        return False


class SellReportView(LoginRequiredMixin,
                    UserPassesTestMixin,
                    SuccessMessageMixin,
                    View):

    def get(self, request, *args, **kwargs):
        f = SellProductFilter(self.request.GET, queryset=SellProduct.objects.filter(is_active=True))
        # sells = SellProduct.objects.all(is_active=True)
        context = {
            # 'filter': f,
            'filter': f,
            'title': 'Sell Report Chart',
        }
        return render(self.request, 'sell_report_chart.html', context)
    
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
        context["purchases"] = PurchaseProduct.objects.filter(is_active=True)
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
    success_message = "%(product_name)s was stocked successfully"

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


class SellsListView(LoginRequiredMixin,
                    UserPassesTestMixin,
                    SuccessMessageMixin,
                    ListView):
    model = SellProduct
    # queryset = SellProduct.objects.filter(is_staff=True)
    context_object_name = 'sells'
    template_name = 'sell.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Sells'
        return context

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
    template_name = 'sell-create.html'
    success_url = 'sell-create'
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
                messages.success(self.request, f'{product_instance.product_name} sold successfully')        
                return redirect('sell-create')
            else:
                messages.warning(self.request, 'Invalid Qunatity')
                return redirect('sell-create')
        messages.warning(self.request, 'Invalid form')        
        return redirect('sell-create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Sell'
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    # def form_valid(self, form):
    #     form.instance.added_by = self.request.user
    #     form.instance.save()
    #     return super(SellProductCreateView, self).form_valid(form)

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
            # 'sells': SellProduct.objects.all()
        }
        return render(self.request, 'sell-create.html', context)

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
                messages.success(self.request, f'{product_instance.product_name} sold successfully')        
                return redirect('sell-list')
            else:
                messages.warning(self.request, 'Invalid Qunatity')
                return redirect('./')
        else:
            messages.warning(self.request, 'Invalid Form')        
            return redirect('./')


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
    template_name = 'sell-create.html'
    success_url = 'sell-list'
    success_message = "%(product_name)s was updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Sell'
        # context["sells"] = SellProduct.objects.filter(is_active=True)
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
    success_url = 'sell-list'
    success_message = "%(name)s was deleted successfully"

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
