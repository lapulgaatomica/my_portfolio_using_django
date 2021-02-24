from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from .models import About, Competency
from .views import (
        HomePageView,
        NewAboutView,
        NewSkillView,
        UpdateAboutView,
        UpdateSkillView,
        DeleteAboutView,
        DeleteSkillView
    )

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
        self.assertNotContains(self.response, 'Add New "About Me"')
        self.assertNotContains(self.response, 'Add New Skill')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            HomePageView.as_view().__name__
        )

class HomepageTestsForSuperUser(TestCase):

    def setUp(self):
        get_user_model().objects.create_superuser(
            username='delesuper',
            email='dele@super.com',
            password='password'
        )
        self.client.login(username='delesuper', password='password')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Add New "About Me"')
        self.assertContains(self.response, 'Add New Skill')

class NewAboutViewTestsForNormalUsers(TestCase):

    def setUp(self):
        url = reverse('new_about')
        self.response = self.client.get(url)

    def test_about_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 302)

class GETNewAboutViewTestsForSuperUsers(TestCase):

    def setUp(self):
        get_user_model().objects.create_superuser(
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

    def test_new_about_url_resolves_new_about_view(self):
        view = resolve('/aboutme/new')
        self.assertEqual(
            view.func.__name__,
            NewAboutView.as_view().__name__
        )


class POSTNewAboutViewTestsForSuperUsers(TestCase):

    def setUp(self):
        get_user_model().objects.create_superuser(
            username='delesuper',
            email='dele@super.com',
            password='password'
        )
        self.client.login(username='delesuper', password='password')
        url = reverse('new_about')
        self.post_response = self.client.post(url, {'paragraph':'I am a new aboutme'}, follow=True)

    def test_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_contains_correct_text(self):
        self.assertContains(self.post_response, 'I am a new aboutme')

class UpdateAboutViewTestsForNormalUsers(TestCase):

    def setUp(self):
        self.about = About.objects.create(
            paragraph='I am a backend developer'
        )
        url = reverse('edit_about', args=[str(self.about.id)])
        self.response = self.client.get(url)

    def test_update_about_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 302)

class UpdateAboutViewTestsForSuperUsers(TestCase):

    def setUp(self):
        get_user_model().objects.create_superuser(
            username='delesuper',
            email='dele@super.com',
            password='password'
        )
        self.client.login(username='delesuper', password='password')
        self.about = About.objects.create(
            paragraph='I am a backend developer'
        )
        url = reverse('edit_about', args=[str(self.about.id)])
        self.response = self.client.get(url)

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
            UpdateAboutView.as_view().__name__
        )

class DeleteAboutViewTestsForNormalUsers(TestCase):

    def setUp(self):
        self.about = About.objects.create(
            paragraph='I am a backend developer'
        )
        url = reverse('delete_about', args=[str(self.about.id)])
        self.response = self.client.get(url)

    def test_delete_about_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 302)

class DeleteAboutViewTestsForSuperUsers(TestCase):

    def setUp(self):
        get_user_model().objects.create_superuser(
            username='delesuper',
            email='dele@super.com',
            password='password'
        )
        self.client.login(username='delesuper', password='password')
        self.about = About.objects.create(
            paragraph='I am a backend developer'
        )
        url = reverse('delete_about', args=[str(self.about.id)])
        self.response = self.client.get(url)

    def test_delete_about_view_status_code_for_super_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_delete_about_template_used(self):
        self.assertTemplateUsed(self.response, 'delete_aboutme.html')

    def test_delete_about_contains_correct_html(self):
        self.assertContains(self.response, 'Delete "About Me"')
        self.assertContains(self.response,
         'Are you sure you want to delete I am a backend developer?')

    def test_delete_about_url_resolves_delete_about_view(self):
        view = resolve(f'/aboutme/{self.about.id}/delete')
        self.assertEqual(
            view.func.__name__,
            DeleteAboutView.as_view().__name__
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

    def test_new_skill_url_resolves_new_skill_view(self):
        view = resolve('/skill/new')
        self.assertEqual(
            view.func.__name__,
            NewSkillView.as_view().__name__
        )

class POSTNewSkillViewTestsForSuperUsers(TestCase):

    def setUp(self):
        get_user_model().objects.create_superuser(
            username='delesuper',
            email='dele@super.com',
            password='password'
        )
        self.client.login(username='delesuper', password='password')
        url = reverse('new_skill')
        self.post_response = self.client.post(url, {'skill':'Devops'}, follow=True)

    def test_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_contains_correct_text(self):
        self.assertContains(self.post_response, 'Devops')

class UpdateSkillViewTestsForNormalUsers(TestCase):

    def setUp(self):
        self.competency = Competency.objects.create(
            skill='Development and Source Control (Docker, Git, Github)'
        )
        url = reverse('edit_skill', args=[str(self.competency.id)])
        self.response = self.client.get(url)

    def test_update_skill_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 302)

class UpdateSkillViewTestsForSuperUsers(TestCase):

    def setUp(self):
        get_user_model().objects.create_superuser(
            username='delesuper',
            email='dele@super.com',
            password='password'
        )
        self.client.login(username='delesuper', password='password')
        self.competency = Competency.objects.create(
            skill='Development and Source Control (Docker, Git, Github)'
        )
        url = reverse('edit_skill', args=[str(self.competency.id)])
        self.response = self.client.get(url)

    def test_update_skill_view_status_code_for_super_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_update_skill_template_used(self):
        self.assertTemplateUsed(self.response, 'update_skill.html')

    def test_update_skill_contains_correct_html(self):
        self.assertContains(self.response,
         'Edit "Development and Source Control (Docker, Git, Github)"')
        self.assertContains(self.response, 'Skill')
        self.assertContains(self.response, 'Edit')

    def test_update_skill_url_resolves_update_skill_view(self):
        view = resolve(f'/skill/{self.competency.id}/edit')
        self.assertEqual(
            view.func.__name__,
            UpdateSkillView.as_view().__name__
        )

class DeleteSkillViewTestsForNormalUsers(TestCase):

    def setUp(self):
        self.competency = Competency.objects.create(
            skill='Development and Source Control (Docker, Git, Github)'
        )
        url = reverse('delete_skill', args=[str(self.competency.id)])
        self.response = self.client.get(url)

    def test_delete_skill_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 302)

class DeleteSkillViewTestsForSuperUsers(TestCase):

    def setUp(self):
        get_user_model().objects.create_superuser(
            username='delesuper',
            email='dele@super.com',
            password='password'
        )
        self.client.login(username='delesuper', password='password')
        self.competency = Competency.objects.create(
            skill='Development and Source Control (Docker, Git, Github)'
        )
        url = reverse('delete_skill', args=[str(self.competency.id)])
        self.response = self.client.get(url)

    def test_delete_skill_view_status_code_for_super_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_delete_skill_template_used(self):
        self.assertTemplateUsed(self.response, 'delete_skill.html')

    def test_delete_skill_contains_correct_html(self):
        self.assertContains(self.response, 'Delete Skill')
        self.assertContains(self.response,
         'Are you sure you want to delete Development and Source Control (Docker, Git, Github)?')

    def test_delete_skill_url_resolves_update_skill_view(self):
        view = resolve(f'/skill/{self.competency.id}/delete')
        self.assertEqual(
            view.func.__name__,
            DeleteSkillView.as_view().__name__
        )

# Remider to actually test submit, edit and delete of data not just the views and templates
# Reminder to folloe the DRY principle and stop writing the exact same login code in every testclass
