from django.conf.urls import url

from .views import CategoryListView

urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='categories'),

]
