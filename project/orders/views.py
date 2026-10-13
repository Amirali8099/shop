import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from products.models import Product
from .models import Order, OrderDetail


def get_cart(user):
    """سبد خرید فعلی کاربر (سفارشی که هنوز نهایی نشده) را برمی‌گرداند یا می‌سازد."""
    cart, _ = Order.objects.get_or_create(user=user, is_ordered=False)
    return cart


@login_required(login_url='login_page')
def cart_view(request):
    cart = get_cart(request.user)
    return render(request, 'orders/cart.html', {'cart': cart})


def add_to_order(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'not_logged_in',
            'icon': 'warning',
            'text': 'برای افزودن به سبد خرید ابتدا وارد حساب کاربری خود شوید.',
            'confirm_button_text': 'ورود به حساب',
        })

    product_id = request.GET.get('product_id')
    count = int(request.GET.get('count', 1))
    product = get_object_or_404(Product, id=product_id)

    cart = get_cart(request.user)
    detail, created = OrderDetail.objects.get_or_create(order=cart, product=product)
    if not created:
        detail.count += count
    else:
        detail.count = count
    detail.save()

    return JsonResponse({
        'status': 'success',
        'icon': 'success',
        'text': f'"{product.title}" به سبد خرید اضافه شد.',
        'confirm_button_text': 'باشه',
    })


@login_required(login_url='login_page')
def remove_order_detail(request):
    detail_id = request.GET.get('detail_id')
    detail = get_object_or_404(OrderDetail, id=detail_id, order__user=request.user)
    detail.delete()

    cart = get_cart(request.user)
    body = render_to_string('orders/_cart_items.html', {'cart': cart}, request=request)
    return JsonResponse({'status': 'success', 'body': body})


@login_required(login_url='login_page')
def change_order_detail(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    detail = get_object_or_404(OrderDetail, id=detail_id, order__user=request.user)

    if state == 'increase':
        detail.count += 1
        detail.save()
    elif state == 'decrease':
        detail.count -= 1
        if detail.count < 1:
            detail.delete()
        else:
            detail.save()

    cart = get_cart(request.user)
    body = render_to_string('orders/_cart_items.html', {'cart': cart}, request=request)
    return JsonResponse({'status': 'success', 'body': body})


@login_required(login_url='login_page')
def checkout_cart(request):
    """با کلیک روی «پردازش و پرداخت»، کاربر را به درگاه زرین‌پال می‌فرستد."""
    cart = get_cart(request.user)

    if not cart.details.exists():
        return redirect('cart')

    amount = cart.total_price
    callback_url = request.build_absolute_uri(reverse('payment_callback'))

    base_url = 'https://sandbox.zarinpal.com' if settings.ZARINPAL_SANDBOX else 'https://api.zarinpal.com'
    try:
        response = requests.post(
            f'{base_url}/pg/v4/payment/request.json',
            json={
                'merchant_id': settings.ZARINPAL_MERCHANT_ID,
                'amount': amount,
                'description': f'پرداخت سفارش شماره {cart.id}',
                'callback_url': callback_url,
            },
            timeout=10,
        )
        data = response.json().get('data', {})
    except requests.RequestException:
        data = {}

    authority = data.get('authority')
    if not authority:
        return render(request, 'orders/payment_result.html', {
            'success': False,
            'message': 'اتصال به درگاه پرداخت برقرار نشد. لطفاً دوباره تلاش کنید.',
        })

    cart.authority = authority
    cart.save()

    gateway_base = 'https://sandbox.zarinpal.com' if settings.ZARINPAL_SANDBOX else 'https://www.zarinpal.com'
    return redirect(f'{gateway_base}/pg/StartPay/{authority}')


def payment_callback(request):
    """آدرسی که زرین‌پال بعد از پرداخت (موفق یا ناموفق) کاربر را به آن برمی‌گرداند."""
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    order = get_object_or_404(Order, authority=authority, is_ordered=False)

    if status != 'OK':
        return render(request, 'orders/payment_result.html', {
            'success': False,
            'message': 'پرداخت توسط شما لغو شد.',
        })

    base_url = 'https://sandbox.zarinpal.com' if settings.ZARINPAL_SANDBOX else 'https://api.zarinpal.com'
    try:
        response = requests.post(
            f'{base_url}/pg/v4/payment/verify.json',
            json={
                'merchant_id': settings.ZARINPAL_MERCHANT_ID,
                'amount': order.total_price,
                'authority': authority,
            },
            timeout=10,
        )
        data = response.json().get('data', {})
    except requests.RequestException:
        data = {}

    if data.get('code') in (100, 101):
        order.is_ordered = True
        order.is_paid = True
        order.ref_id = data.get('ref_id', '')
        order.save()
        return render(request, 'orders/payment_result.html', {
            'success': True,
            'ref_id': order.ref_id,
        })

    return render(request, 'orders/payment_result.html', {
        'success': False,
        'message': 'پرداخت تایید نشد. اگر مبلغی کسر شده ظرف ۷۲ ساعت بازمی‌گردد.',
    })


@login_required(login_url='login_page')
def panel_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()

        new_password = request.POST.get('new_password', '').strip()
        if new_password:
            user.set_password(new_password)

        user.save()

        if new_password:
            return redirect('login_page')

    orders = request.user.orders.filter(is_ordered=True)
    return render(request, 'orders/panel.html', {'orders': orders})
