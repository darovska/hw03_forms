import shutil
import tempfile
from django.test import Client, TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Post, Group, User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()  
        cls.user = User.objects.create(username='Петя')  
        cls.group = Group.objects.create(
            title='Название', 
            slug='Ссылка', 
            description='Описание',  
        )


        cls.post = Post.objects.create(
            text = "Тестовый текст",
            group = cls.group,
            author = cls.user,
         )


    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostCreateFormTests.user)
        self.posts_count = Post.objects.count()

    
    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'group': self.group.id,
            'text': 'Тестовый текст, который длиннее 15 символов',
        }

        response = self.authorized_client.force_login(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), self.posts_count + 1)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            Post.objects.filter(
                author=PostFormTests.user,
                text=self.post.text,
                group=PostFormTests.group.id,
            ).exists()
        )

