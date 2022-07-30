from django.urls import path, re_path

from cars.views import *


urlpatterns = [
    path('', CarHome.as_view(), name='home'),
    path('about', About.as_view(), name='about'),
    path('add_article', AddArticle.as_view(), name='add_article'),
    path('contact', ContactFormView.as_view(), name='contact'),
    path('login', LoginUser.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
    path('register', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('brand/<slug:brand_slug>/', CarBrand.as_view(), name='brand')
]
