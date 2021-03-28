import shutil
import tempfile
from django.test import Client, TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Post, Group

class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        cls.group = Group.objects.create(
            title='Название', 
            slug='Ссылка', 
            description='Описание',  
        )


        cls.post = Post.objects.create(
            text = "Тестовый текст",
            group = cls.group,
            author = User.objects.create(username='Anon'),
         )

        cls.form = TaskCreateForm()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
    
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Anon')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
        }

        response = self.guest_client.post(reverse('index')
        # Проверяем, увеличилось ли число постов
        response = self.assertEqual(Task.objects.count(), tasks_count+1)
        # Проверяем, что создалась запись с нашим слагом
        response = self.assertTrue(
            Task.objects.filter(
                text='Тестовый текст',
                ).exists()
        )