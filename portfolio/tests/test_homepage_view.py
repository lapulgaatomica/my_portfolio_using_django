from django.test import TestCase
from django.urls import reverse, resolve
from .utils import create_pastwork, create_and_login_superuser
from .. import views


class HomepageTests(TestCase):
    response = None

    def setUp(self):
        create_pastwork()
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Odedoyin Akindele')
        self.assertContains(self.response, 'My portfolio app')
        self.assertContains(self.response, 'Check Details')
        self.assertContains(self.response, 'Github Link')
        self.assertContains(self.response, 'Visit the Page')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Add New "About Me"')
        self.assertNotContains(self.response, 'Add New Skill')
        self.assertNotContains(self.response, 'See More Side Projects That I\'ve Done Here...')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            views.HomePageView.as_view().__name__
        )


class HomepageTestsForSuperUser(TestCase):
    response = None

    def setUp(self):
        create_and_login_superuser(self.client)
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Add New "About Me"')
        self.assertContains(self.response, 'Add New Skill')