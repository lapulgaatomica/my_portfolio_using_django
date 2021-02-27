from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from .models import About, Competency, Reason
from .views import (
        HomePageView,
        NewAboutView,
        NewSkillView,
        UpdateAboutView,
        UpdateSkillView,
        DeleteAboutView,
        DeleteSkillView,
        ReasonsView,
        NewReasonView,
        UpdateReasonView,
        DeleteReasonView
    )

def create_and_login_superuser(client):
    get_user_model().objects.create_superuser(
        username='delesuper',
        email='dele@super.com',
        password='password'
    )
    client.login(username='delesuper', password='password')


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
        create_and_login_superuser(self.client)
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

class NewAboutViewTestsForSuperUsers(TestCase):

    def setUp(self):
        create_and_login_superuser(self.client)
        url = reverse('new_about')
        self.response = self.client.get(url)
        self.post_response = self.client.post(url, {'paragraph':'I am a new aboutme'}, follow=True)

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

    def test_post_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_post_template_used(self):
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_post_contains_correct_text(self):
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
            UpdateAboutView.as_view().__name__
        )

    def test_post_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_post_template_used(self):
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_post_contains_correct_text(self):
        self.assertContains(self.post_response, 'Edited I am a backend developer')

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
        self.assertContains(self.response,
         'Are you sure you want to delete I am a backend developer?')

    def test_delete_about_url_resolves_delete_about_view(self):
        view = resolve(f'/aboutme/{self.about.id}/delete')
        self.assertEqual(
            view.func.__name__,
            DeleteAboutView.as_view().__name__
        )

    def test_post_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_post_template_used(self):
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_post_contains_correct_text(self):
        self.assertNotContains(self.post_response, 'I am a backend developer')

class NewSkillViewTestsForNormalUsers(TestCase):

    def setUp(self):
        url = reverse('new_skill')
        self.response = self.client.get(url)

    def test_skill_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 302)

class NewSkillViewTestsForSuperUsers(TestCase):

    def setUp(self):
        create_and_login_superuser(self.client)
        url = reverse('new_skill')
        self.response = self.client.get(url)
        self.post_response = self.client.post(url, {'skill':'Devops'}, follow=True)

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
        create_and_login_superuser(self.client)
        self.competency = Competency.objects.create(
            skill='Development and Source Control (Docker, Git, Github)'
        )
        url = reverse('edit_skill', args=[str(self.competency.id)])
        self.response = self.client.get(url)
        self.post_response = self.client.post(url, {'skill':'Development and Source Control (Docker, Git, Github, Kubernetes)'}, follow=True)

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

    def test_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_contains_correct_text(self):
        self.assertContains(self.post_response, 'Development and Source Control (Docker, Git, Github, Kubernetes)')

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
        create_and_login_superuser(self.client)
        self.competency = Competency.objects.create(
            skill='Development and Source Control (Docker, Git, Github)'
        )
        url = reverse('delete_skill', args=[str(self.competency.id)])
        self.response = self.client.get(url)
        self.post_response = self.client.post(url, follow=True)

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

    def test_post_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_post_template_used(self):
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_post_contains_correct_text(self):
        self.assertNotContains(self.post_response, 'Development and Source Control (Docker, Git, Github)')


class ReasonsViewTestsForNormalUsers(TestCase):

    def setUp(self):
        url = reverse('reasons')
        self.response = self.client.get(url)

    def test_reason_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 302)


class ReasonsViewTestsForSuperUsers(TestCase):

    def setUp(self):
        create_and_login_superuser(self.client)
        url = reverse('reasons')
        self.response = self.client.get(url)

    def test_reasons_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_reasons_page_template(self):
        self.assertTemplateUsed(self.response, 'reason.html')

    def test_reasons_page_contains_correct_html(self):
        self.assertContains(self.response, 'Add New Reason')

    def test_reasons_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Add New "About Me"')
        self.assertNotContains(self.response, 'Add New Skill')

    def test_reasons_page_url_resolves_homepageview(self):
        view = resolve('/reasons')
        self.assertEqual(
            view.func.__name__,
            ReasonsView.as_view().__name__
        )

class NewReasonViewTestsForNormalUsers(TestCase):

    def setUp(self):
        url = reverse('new_reason')
        self.response = self.client.get(url)

    def test_new_reason_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 302)

class NewReasonViewTestsForSuperUsers(TestCase):

    def setUp(self):
        create_and_login_superuser(self.client)
        url = reverse('new_reason')
        self.post_response = self.client.post(url,
                                {'purpose': 'I want to hire you'}, follow=True)


    def test_new_reason_view_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_new_reasons_page_template(self):
        self.assertTemplateUsed(self.post_response, 'reason.html')

    def test_new_reasons_page_contains_correct_html(self):
        self.assertContains(self.post_response, 'I want to hire you')
        self.assertContains(self.post_response, 'Edit')
        self.assertContains(self.post_response, 'Delete')

class UpdateReasonViewTestsForNormalUsers(TestCase):

    def setUp(self):
        self.reason = Reason.objects.create(
            purpose='I want to hire you'
        )
        url = reverse('edit_reason', args=[str(self.reason.id)])
        self.response = self.client.get(url)

    def test_update_reason_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 302)

class UpdateReasonViewTestsForSuperUsers(TestCase):

    def setUp(self):
        create_and_login_superuser(self.client)
        self.reason = Reason.objects.create(
            purpose='I want to hire you'
        )
        url = reverse('edit_reason', args=[str(self.reason.id)])
        self.response = self.client.get(url)
        self.post_response = self.client.post(url, {'purpose':'Want to hire you'}, follow=True)

    def test_update_reason_view_status_code_for_super_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_update_reason_template_used(self):
        self.assertTemplateUsed(self.response, 'update_reason.html')

    def test_update_reason_contains_correct_html(self):
        self.assertContains(self.response,
         'Edit "I want to hire you"')

    def test_update_reason_url_resolves_update_skill_view(self):
        view = resolve(f'/reasons/{self.reason.id}/edit')
        self.assertEqual(
            view.func.__name__,
            UpdateReasonView.as_view().__name__
        )

    def test_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.post_response, 'reason.html')

    def test_contains_correct_text(self):
        self.assertContains(self.post_response, 'Want to hire you')

    def test_does_not_contain_incorrect_text(self):
        self.assertNotContains(self.post_response, 'I want to hire you')

class DeleteReasonViewTestsForNormalUsers(TestCase):

    def setUp(self):
        self.reason = Reason.objects.create(
            purpose='I want to hire you'
        )
        url = reverse('delete_reason', args=[str(self.reason.id)])
        self.response = self.client.get(url)

    def test_delete_reason_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 302)

class DeleteReasonViewTestsForSuperUsers(TestCase):

    def setUp(self):
        create_and_login_superuser(self.client)
        self.reason = Reason.objects.create(
            purpose='I want to hire you'
        )
        url = reverse('delete_reason', args=[str(self.reason.id)])
        self.response = self.client.get(url)
        self.post_response = self.client.post(url, follow=True)

    def test_delete_reason_view_status_code_for_super_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_delete_reason_template_used(self):
        self.assertTemplateUsed(self.response, 'delete_reason.html')

    def test_delete_reason_contains_correct_html(self):
        self.assertContains(self.response, 'Delete "I want to hire you"')
        self.assertContains(self.response, 'Are you sure you want to delete "I want to hire you"?')

    def test_delete_reason_url_resolves_update_skill_view(self):
        view = resolve(f'/reasons/{self.reason.id}/delete')
        self.assertEqual(
            view.func.__name__,
            DeleteReasonView.as_view().__name__
        )

    def test_post_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_post_template_used(self):
        self.assertTemplateUsed(self.post_response, 'reason.html')

    def test_post_contains_correct_text(self):
        self.assertNotContains(self.post_response, 'I want to hire you')
