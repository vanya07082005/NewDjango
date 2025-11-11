"""
Definition of models.
"""


from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User


class Blog(models.Model):
    title=models.CharField(max_length=70,unique_for_date="posted",verbose_name="Заголовок")
    description=models.CharField(verbose_name="Краткое описание",max_length=200)
    price=models.DecimalField(verbose_name="Цена",max_digits=10,  # максимальное количество цифр
        decimal_places=0,  # количество знаков после запятой
        null=True,)
    content=models.TextField(verbose_name="Полное описание")
    posted=models.DateTimeField(default=datetime.now,db_index=True,verbose_name="Опубликован")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image=models.FileField(default="temp.jpg",verbose_name="Путь к картинке")
    def get_absolute_url(self):
        return reverse("blogpost",args=[str(self.id)])
    def __str__(self):
        return self.title
    class Meta:
        db_table="Posts"
        ordering=["-posted"]
        verbose_name="Товар"
        verbose_name_plural="Товары"

admin.site.register(Blog)

class Comment(models.Model):    
    text=models.TextField(verbose_name="Текст комментария")
    date=models.DateTimeField(default=datetime.now,db_index=True,verbose_name="Опубликован")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор")
    post = models.ForeignKey(Blog,  on_delete = models.CASCADE, verbose_name = "Товар")
    def __str__(self):
        return  'Комментарий %d %s к %s'%(self.id,self.author,self.post)
    class Meta:
        db_table="Comment"
        ordering=["-date"]
        verbose_name="Комментарий к товару"
        verbose_name_plural="Комментариик товарам"

admin.site.register(Comment)




class Order(models.Model):
    product = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Товар")
    customer_name = models.CharField(max_length=100, verbose_name="ФИО покупателя")
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    quantity = models.IntegerField(default=1, verbose_name="Количество")
    address = models.TextField(verbose_name="Адрес доставки")
    order_date = models.DateTimeField(default=datetime.now, verbose_name="Дата заказа")
    
    def __str__(self):
        return f'Заказ {self.id} - {self.product.title}'
    
    class Meta:
        db_table = "Orders"
        ordering = ["-order_date"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

admin.site.register(Order)