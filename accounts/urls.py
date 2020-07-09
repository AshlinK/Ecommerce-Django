from .views import (HomeView, products, customer, create_order, update_order,
                    delete_order, login_page, register_page, logout_page,
                    user_page, account_page)
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "accounts"

urlpatterns = [

    # Login and Registration
    path('login/', login_page, name="login"),
    path('logout/', logout_page, name="logout"),
    path('register/', register_page, name="register"),

    path('user/', user_page, name="user"),
    path('', HomeView.as_view(), name="home"),
    path('account/', account_page, name="user_account"),
    path('products/', products, name="products"),
    path('customer/<int:pk>/', customer, name="customer"),

    # CRUD Order
    path('create_order/<int:pk>/', create_order, name="create_order"),
    path('update_order/<int:pk>/', update_order, name="update_order"),
    path('delete_order/<int:pk>/', delete_order, name="delete_order"),
]
# When ever the media url is set, search the document in media root.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
