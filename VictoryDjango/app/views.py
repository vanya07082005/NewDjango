"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import AnketaForm 
from .forms import BlogForm 
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect,get_object_or_404

from django.db import models
from .models import Blog

from .models import Comment # использование модели комментариев
from .forms import CommentForm # использование формы ввода комментария


# Добавьте в views.py
from django.contrib import messages
from .models import Order
from .forms import OrderForm

def order_create(request, product_id):
    product = get_object_or_404(Blog, id=product_id)
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            
           
            return render(request, 'app/index.html', {
                'form': OrderForm(), 
                'product': product,
                'order_success': True
            })
    else:
        form = OrderForm()
    
    return render(request, 'app/order.html', {'form': form, 'product': product})







def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":    # после отправки формы
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()
            return redirect('blog')    # сохранение изменения после добавления полей

    else:
        blogform = BlogForm()
    return render(
        request,
        'app/newpost.html', 
         {
            'blogform': blogform,    # передача формы в шаблон веб-страницы
            'title': 'добавить статью блога',

            'year':datetime.now().year,
         }
    )








def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    
    # Получаем поисковый запрос
    search_query = request.GET.get('search', '')
    
    # Запрос на выбор всех статей блога из модели
    if search_query:
        # Фильтруем посты по заголовку (case-insensitive)
        posts = Blog.objects.filter(title__icontains=search_query)
    else:
        posts = Blog.objects.all()
    
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Каталог товаров',
            'posts': posts,
            'search_query': search_query,  # передаем поисковый запрос в шаблон
            'year': datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    
    # запрос на выбор конкретной статьи по параметру
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm() # создание формы для ввода комментария

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,  # передача конкретной статьи в шаблон веб-страницы
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )


def registration(request):

    """Renders the registration page."""

    assert isinstance(request, HttpRequest)

    if request.method == "POST": # после отправки формы

        regform = UserCreationForm (request.POST)

        if regform.is_valid(): #валидация полей формы

            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы

            reg_f.is_staff = False # запрещен вход в административный раздел

            reg_f.is_active = True # активный пользователь

            reg_f.is_superuser = False # не является суперпользователем

            reg_f.date_joined = datetime.now() # дата регистрации

            reg_f.last_login = datetime.now() # дата последней авторизации

            reg_f.save() # сохраняем изменения после добавления данных

            return redirect('home') # переадресация на главную страницу после регистрации

    else:

        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя

    return render(

        request,

        'app/registration.html',

        {

        'regform': regform, # передача формы в шаблон веб-страницы

        'year':datetime.now().year,

        }

    )

from django.core.mail import send_mail
from django.conf import settings

def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужской', '2': 'Женский'}
    shop_frequency = {
        '1': 'Несколько раз в неделю', 
        '2': 'Несколько раз в месяц',
        '3': 'Несколько раз в сезон', 
        '4': 'Несколько раз в год'
    }
    rating = {
        '1': 'Отлично',
        '2': 'Хорошо',
        '3': 'Удовлетворительно', 
        '4': 'Плохо',
        '5': 'Очень плохо'
    }
    
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['age'] = form.cleaned_data['age']  
            data['gender'] = gender[form.cleaned_data['gender']]
            data['product'] = form.cleaned_data['product'] 
            data['budget'] = form.cleaned_data['budget']  
            data['shop_frequency'] = shop_frequency[form.cleaned_data['shop_frequency']]  
            data['rating'] = rating[form.cleaned_data['rating']]  
            
            if form.cleaned_data['notice']:
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
                
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            
            # Отправка email
            send_mail(
                f'Отзыв от {data["name"]}',
                f'''
                Новый отзыв о товаре:
                Имя: {data['name']}
                Город: {data['city']}
                Товар: {data['product']}
                Оценка: {data['rating']}
                Отзыв: {data['message']}
                ''',
                'noreply@gadgetflow.ru',
                ['vanya07082005@gmail.com'],
                fail_silently=True,
            )
            
            form = None
        
    else:
        form = AnketaForm()
        
    return render(
        request,
        'app/anketa.html',
        {
            'form': form,
            'data': data
        }
    )

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )
def links (request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ссылки',
            'message':'Здесь можно ознакомиться с материалом подробнее',
            'year':datetime.now().year,
        }
    )