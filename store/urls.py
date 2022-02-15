from django.urls import include, path
from store import views

urlpatterns = [
    path('store/', views.getStore, name="store"),
    path('cart/', views.getCart, name="cart"),
    path('checkout/', views.getChekout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('payment/', views.processOrder, name="payment")
]
