from django.contrib.auth import get_user_model
from django.test import TestCase

class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='dele',
            email='dele@dele.com',
            password='password'
        )
        self.assertEqual(user.username, 'dele')
        self.assertEqual(user.email, 'dele@dele.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin = User.objects.create_superuser(
            username='delesuper',
            email='delesuper@delesuper.com',
            password='password'
        )
        self.assertEqual(admin.username, 'delesuper')
        self.assertEqual(admin.email, 'delesuper@delesuper.com')
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
