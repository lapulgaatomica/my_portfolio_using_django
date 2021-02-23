from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from .views import HomePageView, NewAboutView, NewSkillView

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

    # add tests that ascertain that there is "add new "about me"" and "add new skill" buttons on the homepage when superuser is logged in

class NewAboutViewTestsForNormalUsers(TestCase):

    def setUp(self):
        url = reverse('new_about')
        self.response = self.client.get(url)

    def test_about_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 302)

class NewAboutViewTestsForSuperUsers(TestCase):

    def setUp(self):
        self.super_user = get_user_model().objects.create_superuser(
            username='delesuper',
            email='dele@super.com',
            password='password'
        )
        self.client.login(username='delesuper', password='password')
        url = reverse('new_about')
        self.response = self.client.get(url)

    def test_new_about_view_status_code_for_super_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_new_about_template_used(self):
        self.assertTemplateUsed(self.response, 'new_aboutme.html')

    def test_new_about_contains_correct_html(self):
        self.assertContains(self.response, 'Paragraph')
        self.assertContains(self.response, 'Add New "About Me"')
        self.assertContains(self.response, 'Submit')

    def test_new_about_url_resolves_homepageview(self):
        view = resolve('/aboutme/new')
        self.assertEqual(
            view.func.__name__,
            NewAboutView.as_view().__name__
        )

class NewSkillViewTestsForNormalUsers(TestCase):

    def setUp(self):
        url = reverse('new_skill')
        self.response = self.client.get(url)

    def test_skill_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 302)

class NewSkillViewTestsForSuperUsers(TestCase):

    def setUp(self):
        self.super_user = get_user_model().objects.create_superuser(
            username='delesuper',
            email='dele@super.com',
            password='password'
        )
        self.client.login(username='delesuper', password='password')
        url = reverse('new_skill')
        self.response = self.client.get(url)

    def test_new_skill_view_status_code_for_super_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_new_skill_template_used(self):
        self.assertTemplateUsed(self.response, 'new_skill.html')

    def test_new_skill_contains_correct_html(self):
        self.assertContains(self.response, 'Add New Skill')
        self.assertContains(self.response, 'Skill')
        self.assertContains(self.response, 'Add Skill')

    def test_new_skill_url_resolves_homepageview(self):
        view = resolve('/skill/new')
        self.assertEqual(
            view.func.__name__,
            NewSkillView.as_view().__name__
        )

# Reminder to create a newaboutview and newskillview tests for a superuser
# Reminder to create a edit and delete aboutview and skillview tests for a superuser
# Reminder to test models
