from django.conf.urls import include, url


from .views import ProductDetailView
urlpatterns = [
    # Examples:
    # url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^cbv/(?P<pk>\d+)', ProductDetailView.as_view(), name = 'product_detail'),
    url(r'^(?P<id>\d+)', 'products.views.product_detail_view_function', name = 'product_detail_function')
]

