from django.core.cache import cache
from .models import Category


def get_cached_categories():
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.all()
        cache.set('categories', categories, 60 * 60)  # Кеширование на 1 час
    return categories
