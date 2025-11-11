"""
Definition of forms.
"""
from django.db import models
from .models import Comment
from .models import Blog
from .models import Order
from email import message
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
    
class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))


class AnketaForm(forms.Form):
    name=forms.CharField(label="Ваше имя", min_length=2, max_length=100)
    city=forms.CharField(label="Ваш город",min_length=2,max_length=100)
    age=forms.IntegerField(label="Ваш возраст", min_value=18, max_value=100,)
    gender=forms.ChoiceField(label="Ваш пол", 
                             choices=[('1','Мужской'),('2','Женский')],
                             widget=forms.RadioSelect,
                             initial=1)
    product=forms.CharField(label="Название приобретенноого товара", min_length=2,max_length=100)
    budget = forms.IntegerField(label="Цена купленного товара в рублях", 
                            min_value=1,
                            max_value=1000000,
                            initial=1000)
    shop_frequency =forms.ChoiceField(label="Как часто вы пользуетесь нашим интернет-магазином?",
                               choices=(('1','Несколько раз в неделю'),
                                        ('2','Несколько раз в месяц'),
                                        ('3','Несколько раз в сезон'),
                                        ('4','Несколько раз в год')),
                               initial='1')
    rating=forms.ChoiceField(label="Как вы оцениваете товар?",
                               choices=(('1', 'Отлично'),  
                                        ('2', 'Хорошо'),
                                        ('3', 'Удовлетворительно'),
                                        ('4', 'Плохо'),
                                        ('5', 'Очень плохо')),
                               initial='1')
    notice=forms.BooleanField(label="Получать новости сайта на email?",
                              required=False)
    email=forms.EmailField(label='Ваш email',min_length=7,required=False)
    message=forms.CharField(label='Ваш отзыв',
                            widget=forms.Textarea(attrs={'rows':12,'cols':20}))

        
        
class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Оставить отзыв"} # метка к полю формы text

class BlogForm (forms.ModelForm):
    class Meta:
        model = Blog # используемая модель
        fields = ('title','description','price','content','image') # заполняемые поля
        labels = {'title':"Название",'description':"Краткое описание",'price':"Цена",'content':"Полное описание",'image':"Картинка"} # метки к полям формы 




# Добавьте в forms.py после BlogForm

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer_name', 'phone', 'quantity', 'address')
        labels = {
            'customer_name': "ФИО покупателя",
            'phone': "Номер телефона", 
            'quantity': "Количество",
            'address': "Адрес доставки"
        }
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1, 'value': 1}),
            'address': forms.Textarea(attrs={'rows': 4}),
        }

