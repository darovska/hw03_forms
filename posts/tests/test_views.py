from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Group, User

User = get_user_model()

class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Название', 
            slug='test_slug', 
            description='Описание',  
        )


        cls.post = Post.objects.create(
            text = "Тестовый текст",
            group = cls.group,
            author = User.objects.create(username='Anon'),
         )


def setUpClass(self):
    self.templates_pages_names = {
            "index.html": reverse('index'),
            "group.html": reverse('group'),
            "new.html": reverse('new'),
        }
    self.guest_client = Client()
    self.user = User.objects.create_user(username='Anon')
    self.authorized_client = Client()
    self.authorized_client.force_login(self.user)


def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for template, reverse_name in self.templates_page_names.items():
            with self.subTest(template=template, reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template) 


def test_home_page_shows_correct_context(self):
    """Шаблон home сформирован с правильным контекстом."""
    response = self.authorized_client.get(reverse('index'))
    form_fields = {
        # При создании формы поля модели типа TextField 
        # преобразуются в CharField с виджетом forms.Textarea           
        'text': forms.fields.СharField,
        'slug': forms.fields.SlugField,
    }  
      
        # Проверяем, что типы полей формы в словаре context 
        # соответствуют ожиданиям
    for value, expected in form_fields.items():
        with self.subTest(value=value):
            form_field = response.context['form'].fields[value]
            # Проверяет, что поле формы является экземпляром
            # указанного класса
            self.assertIsInstance(form_field, expected)


def test_group_page_shows_correct_context(self):
    """Шаблон group сформирован с правильным контекстом."""
    response = self.authorized_client.get(reverse('group'))
    form_fields = {
        'title': forms.fields.CharField,
        # При создании формы поля модели типа TextField 
        # преобразуются в CharField с виджетом forms.Textarea           
        'decription': forms.fields.CharField,
        'slug': forms.fields.SlugField,
    }  
      
        # Проверяем, что типы полей формы в словаре context 
        # соответствуют ожиданиям
    for value, expected in form_fields.items():
        with self.subTest(value=value):
            form_field = response.context['form'].fields[value]
            # Проверяет, что поле формы является экземпляром
            # указанного класса
            self.assertIsInstance(form_field, expected)


def test_new_page_shows_correct_context(self):
    """Шаблон group сформирован с правильным контекстом."""
    response = self.authorized_client.get(reverse('new'))
    form_fields = {
        'text': forms.fields.CharField,
        # При создании формы поля модели типа TextField 
        # преобразуются в CharField с виджетом forms.Textarea           
        'pub_date': forms.fields.DateTimeField,
    }  
      
    # Проверяем, что типы полей формы в словаре context 
    # соответствуют ожиданиям
    for value, expected in form_fields.items():
        with self.subTest(value=value):
            form_field = response.context['form'].fields[value]
            # Проверяет, что поле формы является экземпляром
            # указанного класса
            self.assertIsInstance(form_field, expected)

