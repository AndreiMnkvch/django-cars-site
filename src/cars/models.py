from django.db import models
from django.urls import reverse


class Car(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name="URL")
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos//%Y/%m/%d")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT)


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


    class Meta:
        verbose_name = 'Крутые тачки 228'
        verbose_name_plural = 'Крутые тачки 228'
        ordering = ['time_update']



class Brand(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Бренд')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name="URL")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand', kwargs={'brand_slug': self.slug})


    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['id']


