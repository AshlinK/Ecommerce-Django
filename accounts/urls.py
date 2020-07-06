from .views import HomeView,products,customer
from django.urls import path

app_name="accounts"
urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path('products/',products,name="products"),
    path('customer/',customer,name="customers"),
]
