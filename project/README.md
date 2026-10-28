
# فروشگاه وولمارت (پروژه‌ی جنگو)

پروژه‌ی فروشگاهی ساخته‌شده بر پایه‌ی قالب HTML وولمارت، با معماری چند اپ ساده.

## راه‌اندازی از صفر

```bash
cd project
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

بعد آدرس `http://127.0.0.1:8000/` رو باز کن. برای پنل مدیریت: `http://127.0.0.1:8000/admin/`

⚠️ **نکته‌ی مهم:** پکیج `Pillow` برای کار کردن فیلدهای تصویر (`ImageField`) لازمه. اگه `requirements.txt` رو نصب نکردی و فقط Django نصب کردی، موقع migrate با خطا مواجه می‌شی.

## ساختار اپ‌ها

| اپ | مسئولیت |
|---|---|
| `home` | صفحه‌ی اصلی |
| `products` | دسته‌بندی، محصولات، نظرات محصول |
| `accounts` | ورود / ثبت‌نام / خروج |
| `articles` | مقالات و نظرات (فقط برای کاربران لاگین‌شده) |
| `pages` | تماس با ما |
| `about_us` | درباره ما (کاملاً استاتیک) |
| `orders` | سبد خرید، پنل کاربری، اتصال به درگاه پرداخت زرین‌پال |
| `wishlist` | لیست علاقه‌مندی‌ها |

## نکات مهم پیکربندی

- **`SECRET_KEY`** توی `settings.py` مقدار پیش‌فرض و ناامنه — قبل از هر انتشار واقعی حتماً عوضش کن.
- **`DEBUG = True`** فقط برای توسعه‌ست؛ روی سرور واقعی باید `False` باشه.
- **زرین‌پال** روی حالت Sandbox (تستی) تنظیم شده (`ZARINPAL_SANDBOX = True` در `settings.py`). برای واقعی‌کردنش، مرچنت‌کد واقعی رو بذار و این مقدار رو `False` کن.

## قبل از تحویل نهایی/انتشار واقعی چی باید اضافه بشه؟
لیست کامل در پاسخ چت آورده شده — خلاصه‌اش: تصاویر واقعی محصولات، متن‌های واقعی (نه لورم ایپسوم)، صفحه‌ی ۴۰۴ سفارشی، پشتیبان‌گیری دیتابیس، و انتقال از SQLite به دیتابیسی مثل PostgreSQL برای هاست واقعی.
## تصاویر پروژه

![تصویر پروژه](./images/Screenshot%202026-10-28%20155754.png)

## تصاویر پروژه

<img width="1920" height="1080" alt="p3" src="https://github.com/user-attachments/assets/fb92a66c-f1db-48ae-95cc-462f81df395b" />
<img width="1920" height="1080" alt="p5" src="https://github.com/user-attachments/assets/05d42d5f-0586-465e-b0f9-7086aa77dc7c" />
<img width="1920" height="1080" alt="p4" src="https://github.com/user-attachments/assets/fdec2498-20ec-4674-b43c-193030108f3b" />
<img width="1920" height="1080" alt="p2" src="https://github.com/user-attachments/assets/a7ae1b24-4728-4647-b87a-0a75e0edd67b" />
<img width="1920" height="1080" alt="p1" src="https://github.com/user-attachments/assets/c68ecbfe-10d8-4df9-b405-5e678963bf61" />
<img width="1920" height="1080" alt="p6" src="https://github.com/user-attachments/assets/5eab2a02-43a5-4260-88d4-0c290a8f581f" />



