from django.test import TestCase
from django.urls import reverse, resolve
from .utils import create_and_login_superuser
from .. import views
from ..models import Competency


class NewSkillViewTestsForNormalUsers(TestCase):
    response = None

    def setUp(self):
        url = reverse('new_skill')
        self.response = self.client.get(url, follow=True)

    def test_skill_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


class NewSkillViewTestsForSuperUsers(TestCase):
    response = None
    post_response = None

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
            views.NewSkillView.as_view().__name__
        )

    def test_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_contains_correct_text(self):
        self.assertContains(self.post_response, 'Devops')


class UpdateSkillViewTestsForNormalUsers(TestCase):
    response = None
    competency = None

    def setUp(self):
        self.competency = Competency.objects.create(
            skill='Development and Source Control (Docker, Git, Github)'
        )
        url = reverse('edit_skill', args=[str(self.competency.id)])
        self.response = self.client.get(url, follow=True)

    def test_update_skill_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


class UpdateSkillViewTestsForSuperUsers(TestCase):
    response = None
    post_response = None
    competency = None

    def setUp(self):
        create_and_login_superuser(self.client)
        self.competency = Competency.objects.create(
            skill='Development and Source Control (Docker, Git, Github)'
        )
        url = reverse('edit_skill', args=[str(self.competency.id)])
        self.response = self.client.get(url)
        self.post_response = self.client.post(url,
                                            {'skill': 'Development and Source Control (Docker, Git, Github, Kubernetes)'},
                                            follow=True)

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
            views.UpdateSkillView.as_view().__name__
        )

    def test_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_contains_correct_text(self):
        self.assertContains(self.post_response, 'Development and Source Control (Docker, Git, Github, Kubernetes)')


class DeleteSkillViewTestsForNormalUsers(TestCase):
    response = None
    competency = None

    def setUp(self):
        self.competency = Competency.objects.create(
            skill='Development and Source Control (Docker, Git, Github)'
        )
        url = reverse('delete_skill', args=[str(self.competency.id)])
        self.response = self.client.get(url, follow=True)

    def test_delete_skill_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


class DeleteSkillViewTestsForSuperUsers(TestCase):
    response = None
    post_response = None
    competency = None

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
            views.DeleteSkillView.as_view().__name__
        )

    def test_post_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_post_template_used(self):
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_post_contains_correct_text(self):
        self.assertNotContains(self.post_response, 'Development and Source Control (Docker, Git, Github)')
