from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, User
User = get_user_model()


class PostsURLTests(TestCase):
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
    self.guest_client = Client()
    self.user = User.objects.create_user(username='Anon')
    self.authorized_client = Client()
    self.authorized_client.force_login(self.user)


    def test_url_exists_at_desired_location(self):
        """Страница доступна любому пользователю."""
        urls = {
            'index.html': reverse('index'),
            "group.html": reverse('group', kwargs={'slug': 'slug'}),
            "new.html": reverse('new'),
        }
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get('')
                self.assertEqual(response.status_code, 200)


    def test_new_post_url_exists_at_desired_location(self):
        """Страница new_post.html доступна авторизованному пользователю."""
        response = self.authorized_client.get('new/')
        self.assertEqual(response.status_code, 200)


    def test_new_post_url_redirect_anonymous(self):
        """Страница new_post.html перенаправляет анонимного
        пользователя.
        """
        response = self.guest_client.get('new/')
        self.assertEqual(response.status_code, 302)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
                'index.html': '',
                'group_posts.html': 'group/test_slug>/',
                'new_post.html': 'new/',
            }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

class StaticURLTests(TestCase):
    def test_homepage(self):
        # Создаем экземпляр клиента
        self.guest_client = Client()
        # Делаем запрос к главной странице и проверяем статус
        response = self.guest_client.get('/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)

