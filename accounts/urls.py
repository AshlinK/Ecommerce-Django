from .views import home,products,customer
from django.urls import path

app_name="accounts"
urlpatterns = [
    path('',home),
    path('products/',products,name="products"),
    path('customer/',customer,name="customers"),
]
