from django.test import TestCase
from django.urls import reverse, resolve
from .. import views
from .utils import create_and_login_superuser, create_pastwork


class PastWorksViewTests(TestCase):
    response = None

    def setUp(self):
        create_pastwork()
        url = reverse('pastworks')
        self.response = self.client.get(url)

    def test_pastworks_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_pastworks_page_template(self):
        self.assertTemplateUsed(self.response, 'pastworks.html')

    def test_pastworks_page_contains_correct_html(self):
        self.assertContains(self.response, 'My portfolio app')
        self.assertContains(self.response, 'Check Details')
        self.assertContains(self.response, 'Github Link')
        self.assertContains(self.response, 'Visit the Page')

    def test_pastworks_page_does_not_contains_correct_html(self):
        self.assertNotContains(self.response, 'Edit')
        self.assertNotContains(self.response, 'Delete')

    def test_pastworks_page_url_resolves_pageview(self):
        view = resolve('/pastworks')
        self.assertEqual(
            view.func.__name__,
            views.PastWorksView.as_view().__name__
        )

    def test_pastworks_view_for_super_users(self):
        create_and_login_superuser(self.client)
        url = reverse('pastworks')
        response = self.client.get(url)
        self.assertContains(response, 'Edit')
        self.assertContains(response, 'Delete')


class PastWorkViewTests(TestCase):
    response = None
    past_work = None

    def setUp(self):
        self.past_work = create_pastwork()
        url = reverse('pastwork', args=[str(self.past_work.id)])
        self.response = self.client.get(url)

    def test_pastwork_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_pastwork_page_template(self):
        self.assertTemplateUsed(self.response, 'pastwork.html')

    def test_pastwork_page_contains_correct_html(self):
        self.assertContains(self.response, 'My portfolio app')
        self.assertContains(self.response, 'Github Link')
        self.assertContains(self.response, 'Visit the Page')

    def test_pastwork_page_does_not_contains_correct_html(self):
        self.assertNotContains(self.response, 'Check Details')

    def test_pastwork_page_url_resolves_pageview(self):
        view = resolve(f'/pastwork/{self.past_work.id}')
        self.assertEqual(
            view.func.__name__,
            views.PastWorkView.as_view().__name__
        )


class NewPastWorkViewForNormalUsers(TestCase):
    response = None

    def setUp(self):
        url = reverse('new_pastwork')
        self.response = self.client.get(url, follow=True)

    def test_new_pastwork_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 404)


class NewPastWorkViewForSuperUsers(TestCase):
    response = None
    post_response = None

    def setUp(self):
        create_and_login_superuser(self.client)
        url = reverse('new_pastwork')
        self.response = self.client.get(url, follow=True)
        self.post_response = self.client.post(url, {'name': 'Portfolio app', 'description': 'A portfolio app',
                                                    'github_link': 'https://github.com', 'page_link': 'https://app.com'}
                                              , follow=True)

    def test_new_pastwork_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.post_response.status_code, 200)

    def test_new_pastwork_template_used(self):
        self.assertTemplateUsed(self.response, 'new_pastwork.html')
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_new_pastwork_contains_correct_html(self):
        self.assertContains(self.response, 'Add Past Work')
        self.assertContains(self.post_response, 'Portfolio app')
        self.assertContains(self.post_response, 'A portfolio app')

    def test_new_pastwork_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'A portfolio app')

    def test_new_pastwork_url_resolves_new_pastwork_view(self):
        view = resolve('/pastwork/new')
        self.assertEqual(
            view.func.__name__,
            views.NewPastWorkView.as_view().__name__
        )


class UpdatePastWorkViewTestsForNormalUsers(TestCase):
    response = None
    past_work = None

    def setUp(self):
        self.past_work = create_pastwork()
        url = reverse('update_pastwork', args=[str(self.past_work.id)])
        self.response = self.client.get(url, follow=True)

    def test_update_pastwork_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 404)


class UpdatePastWorkViewTestsForSuperUsers(TestCase):
    response = None
    post_response = None
    past_work = None

    def setUp(self):
        create_and_login_superuser(self.client)
        self.past_work = create_pastwork()
        url = reverse('update_pastwork', args=[str(self.past_work.id)])
        self.response = self.client.get(url, follow=True)
        self.post_response = self.client.post(url, {'name': 'Portfolio app edited',
                                                    'description': 'An edited portfolio app',
                                                    'github_link': 'https://github.com',
                                                    'page_link': 'https://app.com'}, follow=True)

    def test_update_pastwork_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.post_response.status_code, 200)

    def test_update_pastwork_template_used(self):
        self.assertTemplateUsed(self.response, 'update_pastwork.html')
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_update_pastwork_contains_correct_html(self):
        self.assertContains(self.response, f'Edit {self.past_work.name}')
        self.assertContains(self.post_response, 'Portfolio app edited')

    def test_update_pastwork_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Portfolio app edited')

    def test_update_pastwork_url_resolves_new_pastwork_view(self):
        view = resolve(f'/pastwork/{self.past_work.id}/edit')
        self.assertEqual(
            view.func.__name__,
            views.UpdatePastWorkView.as_view().__name__
        )


class DeletePastWorkViewTestsForNormalUsers(TestCase):
    response = None
    past_work = None

    def setUp(self):
        self.past_work = create_pastwork()
        url = reverse('delete_pastwork', args=[str(self.past_work.id)])
        self.response = self.client.get(url, follow=True)

    def test_delete_pastwork_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 404)


class DeletePastWorkViewTestsForSuperUsers(TestCase):
    response = None
    post_response = None
    past_work = None

    def setUp(self):
        create_and_login_superuser(self.client)
        self.past_work = create_pastwork()
        url = reverse('delete_pastwork', args=[str(self.past_work.id)])
        self.response = self.client.get(url)
        self.post_response = self.client.post(url, follow=True)

    def test_delete_pastwork_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.post_response.status_code, 200)

    def test_delete_pastwork_template_used(self):
        self.assertTemplateUsed(self.response, 'delete_pastwork.html')
        self.assertTemplateUsed(self.post_response, 'home.html')

    def test_delete_pastwork_contains_correct_html(self):
        self.assertContains(self.response, f'Delete {self.past_work.name}')

    def test_delete_pastwork_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.post_response, f'{self.past_work.name}')

    def test_delete_pastwork_url_resolves_new_pastwork_view(self):
        view = resolve(f'/pastwork/{self.past_work.id}/delete')
        self.assertEqual(
            view.func.__name__,
            views.DeletePastWorkView.as_view().__name__
        )