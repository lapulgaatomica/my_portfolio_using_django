from django.test import TestCase
from django.urls import reverse, resolve
from .utils import create_and_login_superuser
from .. import views
from ..models import Reason


class ReasonsViewTestsForNormalUsers(TestCase):
    response = None

    def setUp(self):
        url = reverse('reasons')
        self.response = self.client.get(url, follow=True)

    def test_reason_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 404)


class ReasonsViewTestsForSuperUsers(TestCase):
    response = None

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

    def test_reasons_page_url_resolves_pageview(self):
        view = resolve('/reasons')
        self.assertEqual(
            view.func.__name__,
            views.ReasonsView.as_view().__name__
        )


class NewReasonViewTestsForNormalUsers(TestCase):
    response = None

    def setUp(self):
        url = reverse('new_reason')
        self.response = self.client.get(url, follow=True)

    def test_new_reason_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 404)


class NewReasonViewTestsForSuperUsers(TestCase):
    post_response = None

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
    response = None
    reason = None

    def setUp(self):
        self.reason = Reason.objects.create(
            purpose='I want to hire you'
        )
        url = reverse('edit_reason', args=[str(self.reason.id)])
        self.response = self.client.get(url, follow=True)

    def test_update_reason_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


class UpdateReasonViewTestsForSuperUsers(TestCase):
    response = None
    post_response = None
    reason = None

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
        self.assertContains(self.response, 'Edit "I want to hire you"')

    def test_update_reason_url_resolves_update_skill_view(self):
        view = resolve(f'/reasons/{self.reason.id}/edit')
        self.assertEqual(
            view.func.__name__,
            views.UpdateReasonView.as_view().__name__
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
    response = None
    reason = None

    def setUp(self):
        self.reason = Reason.objects.create(
            purpose='I want to hire you'
        )
        url = reverse('delete_reason', args=[str(self.reason.id)])
        self.response = self.client.get(url, follow=True)

    def test_delete_reason_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


class DeleteReasonViewTestsForSuperUsers(TestCase):
    response = None
    post_response = None
    reason = None

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
            views.DeleteReasonView.as_view().__name__
        )

    def test_post_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_post_template_used(self):
        self.assertTemplateUsed(self.post_response, 'reason.html')

    def test_post_contains_correct_text(self):
        self.assertNotContains(self.post_response, 'I want to hire you')