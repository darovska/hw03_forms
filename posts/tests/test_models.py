from django.test import TestCase
from posts.models import Post, User, Group


class PostsModelsTest(TestCase):
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

    def test_verbose_name(self):
        post = PostsModelsTest.post
        field_verboses = {
            'text': "Текст",
            'group': "Группа",
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected    
                )


    def test_help_text(self):
        post = PostsModelsTest.post
        field_help_texts = {
            'text': "Напишите текст",
            'group': "Выберите группу",
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected
                )


    def test_str_post(self):
        post = PostsModelsTest.post
        text = post.text
        self.assertEqual(str(post), text[:15])


    def _test_str_group(self):
        group = PostsModelsTest.group
        tittle = str(group)
        self.assertEqual(tittle, group.tittle)

