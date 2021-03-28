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

        templates_pages_names = {
            "index.html": reverse('index'),
            "new.html": reverse('new_post'),
            "group.html": (
                reverse('group_posts',kwargs={'slug': 'test-slug'})
            ),
        }        

        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='anon')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

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


    def test_pages_use_correct_template(self):    
        """URL-адрес использует соответствующий шаблон."""
        for template, reverse_name in self.templates_page_names.items():
            with self.subTest(template=template, reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template) 


    def test_index_page_shows_correct_context(self):
        """Шаблон home сформирован с правильным контекстом."""
        response = PostPagesTest.authorized_client.get(reverse('index'))
        post_object = context.get['posts'][0]
        post_group_0 = post_object.group
        post_text_0 = post_object.text
        post_author_0 = post_object.author
        self.assertEqual(post_group_0, PostPagesTests.group)
        self.assertEqual(post_text_0, PostPagesTests.post)
        self.assertEqual(post_author_0, PostPagesTests.user)


    def test_group_list_pages_shows_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = PostPagesTests.authorized_client.get(reverse('group_posts',kwargs={'slug': 'test-slug'}))
        response_text = context['posts'][0].text
        response_author = context['posts'][0].author
        response_group = context['group']
        self.assertEqual(response_text, 'Текстовый текст')
        self.assertEqual(response_author.username, 'gamble')
        self.assertEqual(response_group.title, 'название')

