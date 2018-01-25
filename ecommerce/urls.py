from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from carts.views import CartView, ItemCountView, CheckoutView, FinalCheckoutView
from orders.views import AddressSelectFormView, UserAddressCreateView, OrderList, OrderDetailView

urlpatterns = [
    # Examples:
    url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^contact/$', 'newsletter.views.contact', name='contact'),
    url(r'^about/$', 'ecommerce.views.about', name='about'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^categories/', include('products.urls_categories')),
    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^orders/$', OrderList.as_view(), name='order_list'),
    url(r'^orders/(?P<pk>\d+)/$', OrderDetailView.as_view(), name='order_detail'),
    url(r'^cart/item_count/$', ItemCountView.as_view(), name='item_count'),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^checkout/address/$', AddressSelectFormView.as_view(), name='order_address'),
    url(r'^checkout/address/add/$', UserAddressCreateView.as_view(), name='create_address'),
    url(r'^checkout/final/$', FinalCheckoutView.as_view(), name='final_checkout')
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
