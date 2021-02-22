from django.test import TestCase
from django.urls import reverse, resolve

from .views import HomePageView

class HomepageTests(TestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Odedoyin Akindele')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'lmao')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            HomePageView.as_view().__name__
        )

class NewAboutViewTestsForNormalUsers(TestCase):

    def setUp(self):
        url = reverse('new_about')
        self.response = self.client.get(url)

    def test_about_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 302)


class NewSkillViewTestsForNormalUsers(TestCase):

    def setUp(self):
        url = reverse('new_skill')
        self.response = self.client.get(url)

    def test_skill_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 302)

#Reminder to create an newaboutview and newskillview tests for a superuser
