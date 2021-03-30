import shutil
import tempfile
from django import forms
from django.test import Client, TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Post, Group, User


class PostCreateFormTests(TestCase):
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


    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'group': self.group.id,
            'text': 'Тестовый текст, длиннее 15 символов',
        }

        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                author=PostCreateFormTests.user,
                text=self.post.text,
                group=PostCreateFormTests.group.id,
            ).exists()
        )

