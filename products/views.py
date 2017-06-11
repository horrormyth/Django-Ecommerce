from django.contrib import messages
from django.db.models import Q

from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .forms import VariationInventoryFormSet
from .mixins import LoginRequiredMixin
from .models import Product, Variation


# Editing for admin
class VariationListView(LoginRequiredMixin, ListView):
    model = Variation
    queryset = Variation.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(VariationListView, self).get_context_data(*args, **kwargs)
        context['formset'] = VariationInventoryFormSet(queryset = self.get_queryset())

        return context

    # Get product specific inventory list
    def get_queryset(self, *args, **kwargs):
        product_pk = self.kwargs.get('pk')
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            queryset = Variation.objects.filter(product=product)
        return queryset

    # Handle inventory update form and post
    def post(self, request, *args, **kwargs):
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save(commit = False)
            # Handle new item addition as well
            for form in formset:
                new_item = form.save(commit = False)
                # if new_item.title:
                product_pk = self.kwargs.get('pk')
                product = get_object_or_404(Product, pk=product_pk)
                new_item.product = product
                new_item.save()
            messages.success(request, 'Your inventory and pricing has been updated')
            return redirect('products')

        raise Http404




class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')

        return context

    # For search implementation overwrite the queryset method
    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
            # Fall back search implementation with price
            try:
                qs2 = self.model.objects.filter(
                    Q(price=query)
                )
                qs = (qs | qs2).distinct()
            except:
                pass
        return qs


class ProductDetailView(DetailView):
    model = Product


# def product_detail_view_function(request, id):
#     # product_instance = Product.objects.get(id = id)
#     product_instance = get_object_or_404(Product, id = id)
#
#     try:
#         product_instance = Product.objects.get(id=id)
#     except Product.DoesNotExist:
#         raise Http404
#     except:
#         raise Http404
#
#     template = 'products/product_detail.html'
#     context = {
#         'object': product_instance
#     }
#     return render(request, template, context)
