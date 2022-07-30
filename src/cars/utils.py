from django.db.models import Count

from .models import *
from django.core.cache import cache

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_article'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    ]


class DataMixin:
    paginate_by = 10

    def get_user_context(self, **kwargs):
        context = kwargs
        brands = cache.get('brands')
        if not brands:
            brands = Brand.objects.filter(car__is_published=True).annotate(number_of_cars=Count('car'))
            cache.set('brands', brands, 60)
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['brands'] = brands
        if 'brand_selected' not in context:
            context['brand_selected'] = 0
        return context

