import datetime
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import request, JsonResponse
from .models import *
import json


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {"get_cart_items": 0, "get_cart_total": 0}
    cart_items = order['get_cart_items']
    for i in cart:
        try:
            cart_items += cart[i]["quantity"]
            products = Product.objects.get(id=i)
            total = (products.price * cart[i]["quantity"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "imageUrl": product.imageUrl,
                },
                "quantity": cart[i]["quantity"],
                "getTotal": total
            }
            items.append(item)
            if not product.digital:
                order["shipping"] = True
        except:
            pass
    return {"items": items, "order": order, "cart_items": cart_items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}
