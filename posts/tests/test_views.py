from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User

class PostsPagesTests(TestCase):
    templates_pages_names = {
            "index.html": reverse('index'),
            "new.html": reverse('new_post'),
            "group.html": (
                reverse('group_posts',kwargs={'slug': 'test_slug'})
            ),
        }        

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='Anon')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Название', 
            slug='test_slug', 
            description='Описание',  
        )


        cls.post=Post.objects.create(
            text="Тестовый текст",
            group = cls.group,
            author = cls.user,
        )


    def test_pages_use_correct_template(self):    
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            "index.html": reverse('index'),
            "new.html": reverse('new_post'),
            "group.html": (
                reverse('group_posts',kwargs={'slug': 'test_slug'})
            ),
        }        
        for template, reverse_name in self.templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template) 


    def test_home_page_shows_correct_context(self):
        """Шаблон home сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('index'))
        post = self.post
        response_post = response.context['posts'][0]
        self.assertEqual(post, response_post)


    def test_group_page_shows_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={'slug': 'test_slug'}))
        self.assertEqual(response.context['group'].title, self.group.title)
        self.assertEqual(response.context['group'].description, 'Описание')
        self.assertEqual(response.context['group'].slug, self.group.slug)


    def test_new_page_shows_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            # При создании формы поля модели типа TextField
            # преобразуются в CharField с виджетом forms.Textarea
            'group': forms.fields.ChoiceField,
        }
        # Проверяем, что типы полей формы в словаре context
        # соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)

