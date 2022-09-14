import os

from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from cars.forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from cars.utils import *
import logging


logger = logging.getLogger('feedback')


class CarHome(DataMixin, ListView):
    paginate_by = 3
    model = Car
    template_name = 'cars/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return context | c_def

    def get_queryset(self):
        return Car.objects.filter(is_published=True).select_related('brand')


class About(DataMixin, ListView):
    template_name = 'cars./about.html'
    model = Brand

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О сайте')
        return context | c_def


class AddArticle(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'cars/add_article.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return context | c_def


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'cars/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return context | c_def

    def form_valid(self, form):
        logger.info(form.cleaned_data)
        return redirect('home')


class ShowPost(DataMixin, DetailView):
    model = Car
    template_name = 'cars/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return context | c_def


class CarBrand(DataMixin, ListView):
    model = Car
    template_name = 'cars/index.html'
    context_object_name = 'posts'
    allow_empty = True

    def get_queryset(self):
        return Car.objects.filter(brand__slug=self.kwargs['brand_slug'], is_published=True).select_related('brand')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].brand),
                                      brand_selected=context['posts'][0].brand_id)
        return context | c_def

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена</h1>')

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'cars/register.html'
    success_url = reverse_lazy('login')


    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return context | c_def

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'cars/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('/login')
