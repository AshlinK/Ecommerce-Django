from .views import HomeView,products,customer,create_order,update_order,delete_order
from django.urls import path

app_name="accounts"

urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path('products/',products,name="products"),
    path('customer/<int:pk>/',customer,name="customer"),

    # CRUD Order
    path('create_order/<int:pk>/',create_order,name="create_order"),
    path('update_order/<int:pk>/',update_order,name="update_order"),
    path('delete_order/<int:pk>/',delete_order,name="delete_order"),
]
