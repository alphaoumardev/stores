import datetime
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import request, JsonResponse
from .models import *
import json
from .utils import *


# Create your views here.
def getStore(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookieCart(request)
        cart_items = cookie_data['cart_items']
    context = {"products": products, "cart_items": cart_items, "shipping": False}
    return render(request, 'store.html', context)


def getCart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookieCart(request)
        cart_items = cookie_data['cart_items']
        order = cookie_data['order']
        items = cookie_data['items']

    context = {"items": items, "order": order, "cart_items": cart_items, "shipping": False}
    return render(request, 'cart.html', context)


@csrf_exempt
def getChekout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookieCart(request)
        cart_items = cookie_data['cart_items']
        order = cookie_data['order']
        items = cookie_data['items']
    context = {"items": items, "cart_items": cart_items, "order": order, "shipping": False}
    return render(request, 'checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.data)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        print("The user is not logged in")
        print("Cookies", request.COOKIES)
        name = data['form']['name']
        email = data['form']['email']
        cookie_data = cookieCart(request)
        items = cookie_data['items']
        customer, created = Customer.objects.get_or_create(
            email=email
        )
        customer.name = name
        customer.save()
        order = Order.objects.create(
            customer=customer,
            complete=False
        )
        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            OrderItem.objects.create(
                product=product,
                order=order,
                quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity'])
            )

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            detailed_address=data['shipping']['detailed_address'],
        )
    return JsonResponse("Payment complete", safe=False)
