from django import template
from cars.models import *


register = template.Library()
#
# @register.simple_tag(name='getbrands')
# def get_brands():
#     return Brand.objects.all()
#
#
# @register.inclusion_tag('cars/list_brands.html')
# def show_brands(sort=None, brand_selected=0):
#     if sort == None:
#         brands = Brand.objects.all()
#     else:
#         brands = Brand.objects.order_by(sort)
#     return {'brands': brands, 'brand_selected': brand_selected}
