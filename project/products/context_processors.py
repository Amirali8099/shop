def all_categories(request):
    """همه‌ی دسته‌بندی‌های محصولات را برای نمایش در منوی هدر برمی‌گرداند."""
    from .models import Category
    return {'categories': Category.objects.all()}
