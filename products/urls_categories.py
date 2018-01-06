from django.conf.urls import url

from .views import CategoryListView, CategoryDetailView

urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='categories'),
    url(r'^(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(), name='category_detail'),
]
