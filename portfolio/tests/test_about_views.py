from django.test import TestCase
from django.urls import reverse, resolve
from .utils import create_and_login_superuser
from .. import views
from ..models import About


class NewAboutViewTestsForNormalUsers(TestCase):
    response = None

    def setUp(self):
        url = reverse('new_about')
        self.response = self.client.get(url, follow=True)

    def test_about_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


class NewAboutViewTestsForSuperUsers(TestCase):
    response = None
    post_response = None

    def setUp(self):
        create_and_login_superuser(self.client)
        url = reverse('new_about')
        self.response = self.client.get(url)
        self.post_response = self.client.post(url, {'paragraph': 'I am a new aboutme'}, follow=True)

    def test_new_about_view_status_code_for_super_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_new_about_template_used(self):
        self.assertTemplateUsed(self.response, 'new_aboutme.html')

    def test_new_about_contains_correct_html(self):
        self.assertContains(self.response, 'Paragraph')
        self.assertContains(self.response, 'Add New "About Me"')
        self.assertContains(self.response, 'Submit')

    def test_new_about_url_resolves_new_about_view(self):
        view = resolve('/aboutme/new')
        self.assertEqual(
            view.func.__name__,
            views.NewAboutView.as_view().__name__
        )

    def test_post_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_post_template_used(self):
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_post_contains_correct_text(self):
        self.assertContains(self.post_response, 'I am a new aboutme')


class UpdateAboutViewTestsForNormalUsers(TestCase):
    response = None
    about = None

    def setUp(self):
        self.about = About.objects.create(
            paragraph='I am a backend developer'
        )
        url = reverse('edit_about', args=[str(self.about.id)])
        self.response = self.client.get(url, follow=True)

    def test_update_about_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


class UpdateAboutViewTestsForSuperUsers(TestCase):
    response = None
    post_response = None
    about = None

    def setUp(self):
        create_and_login_superuser(self.client)
        self.about = About.objects.create(
            paragraph='I am a backend developer'
        )
        url = reverse('edit_about', args=[str(self.about.id)])
        self.response = self.client.get(url)
        self.post_response = self.client.post(url, {'paragraph': 'Edited I am a backend developer'}, follow=True)

    def test_update_about_view_status_code_for_super_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_update_about_template_used(self):
        self.assertTemplateUsed(self.response, 'update_aboutme.html')

    def test_update_about_contains_correct_html(self):
        self.assertContains(self.response, 'Edit "About Me"')
        self.assertContains(self.response, 'Paragraph')
        self.assertContains(self.response, 'I am a backend developer')

    def test_update_about_url_resolves_update_about_view(self):
        view = resolve(f'/aboutme/{self.about.id}/edit')
        self.assertEqual(
            view.func.__name__,
            views.UpdateAboutView.as_view().__name__
        )

    def test_post_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_post_template_used(self):
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_post_contains_correct_text(self):
        self.assertContains(self.post_response, 'Edited I am a backend developer')


class DeleteAboutViewTestsForNormalUsers(TestCase):
    response = None
    about = None

    def setUp(self):
        self.about = About.objects.create(
            paragraph='I am a backend developer'
        )
        url = reverse('delete_about', args=[str(self.about.id)])
        self.response = self.client.get(url, follow=True)

    def test_delete_about_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


class DeleteAboutViewTestsForSuperUsers(TestCase):
    response = None
    post_response = None
    about = None

    def setUp(self):
        create_and_login_superuser(self.client)
        self.about = About.objects.create(
            paragraph='I am a backend developer'
        )
        url = reverse('delete_about', args=[str(self.about.id)])
        self.response = self.client.get(url)
        self.post_response = self.client.post(url, follow=True)

    def test_delete_about_view_status_code_for_super_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_delete_about_template_used(self):
        self.assertTemplateUsed(self.response, 'delete_aboutme.html')

    def test_delete_about_contains_correct_html(self):
        self.assertContains(self.response, 'Delete "About Me"')
        self.assertContains(self.response, 'Are you sure you want to delete I am a backend developer?')

    def test_delete_about_url_resolves_delete_about_view(self):
        view = resolve(f'/aboutme/{self.about.id}/delete')
        self.assertEqual(
            view.func.__name__,
            views.DeleteAboutView.as_view().__name__
        )

    def test_post_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_post_template_used(self):
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_post_contains_correct_text(self):
        self.assertNotContains(self.post_response, 'I am a backend developer')