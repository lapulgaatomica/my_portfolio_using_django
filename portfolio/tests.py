from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from .models import About, Competency, Reason, Message, PastWork
from . import views


def create_and_login_superuser(client):
    get_user_model().objects.create_superuser(
        username='delesuper',
        email='dele@super.com',
        password='password'
    )
    client.login(username='delesuper', password='password')


def create_pastwork():
    return PastWork.objects.create(name='Portfolio', description='My portfolio app',
                                   github_link='https://github.com', page_link='https://app.com')


class HomepageTests(TestCase):

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
        self.response = self.client.get(url, follow=True)

    def test_about_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


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
            views.NewAboutView.as_view().__name__
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
        self.response = self.client.get(url, follow=True)

    def test_update_about_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


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
            views.UpdateAboutView.as_view().__name__
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
        self.response = self.client.get(url, follow=True)

    def test_delete_about_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


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


class NewSkillViewTestsForNormalUsers(TestCase):

    def setUp(self):
        url = reverse('new_skill')
        self.response = self.client.get(url, follow=True)

    def test_skill_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


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
            views.NewSkillView.as_view().__name__
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
        self.response = self.client.get(url, follow=True)

    def test_update_skill_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


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
            views.UpdateSkillView.as_view().__name__
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
        self.response = self.client.get(url, follow=True)

    def test_delete_skill_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


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
            views.DeleteSkillView.as_view().__name__
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
        self.response = self.client.get(url, follow=True)

    def test_reason_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 404)


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

    def test_reasons_page_url_resolves_pageview(self):
        view = resolve('/reasons')
        self.assertEqual(
            view.func.__name__,
            views.ReasonsView.as_view().__name__
        )


class NewReasonViewTestsForNormalUsers(TestCase):
    def setUp(self):
        url = reverse('new_reason')
        self.response = self.client.get(url, follow=True)

    def test_new_reason_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 404)


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
        self.response = self.client.get(url, follow=True)

    def test_update_reason_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


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
    def setUp(self):
        self.reason = Reason.objects.create(
            purpose='I want to hire you'
        )
        url = reverse('delete_reason', args=[str(self.reason.id)])
        self.response = self.client.get(url, follow=True)

    def test_delete_reason_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


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
            views.DeleteReasonView.as_view().__name__
        )

    def test_post_status_code(self):
        self.assertEqual(self.post_response.status_code, 200)

    def test_post_template_used(self):
        self.assertTemplateUsed(self.post_response, 'reason.html')

    def test_post_contains_correct_text(self):
        self.assertNotContains(self.post_response, 'I want to hire you')


class SendMessageViewTests(TestCase):
    def setUp(self):
        Reason.objects.create(purpose='I want to hire you')
        url = reverse('send_message')
        self.response = self.client.post(url,
                                         {'reason': '1',
                                          'name': 'Jane Doe',
                                          'email': 'jane@doe.com',
                                          'message': 'Hey Dele'},
                                         follow=True)
        self.message_query = Message.objects.get(id=1)

    def test_send_message_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_redirect_template_used(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_sent_message_template_contains_correct_html(self):
        self.assertContains(self.response, 'Your message was sent successfully, expect a feedback ASAP!!!')

    def test_message_in_database(self):
        self.assertTrue(self.message_query.name, 'Jane Doe')
        self.assertTrue(self.message_query.reason, 'I want to hire you')
        self.assertTrue(self.message_query.email, 'jane@doe.com')
        self.assertTrue(self.message_query.message, 'Hey Dele')


class MessagesReceivedViewTestsForNormalUsers(TestCase):
    def setUp(self):
        reason = Reason.objects.create(purpose='I want to hire you')
        Message.objects.create(reason=reason, name='Jane Doe', email='jane@doe.com', message='Hey Dele')
        url = reverse('received_messages')
        self.response = self.client.get(url, follow=True)

    def test_messages_received_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


class MessagesReceivedViewTestsForSuperUsers(TestCase):
    def setUp(self):
        create_and_login_superuser(self.client)
        reason = Reason.objects.create(purpose='I want to hire you')
        Message.objects.create(reason=reason, name='Jane Doe', email='jane@doe.com', message='Hey Dele')
        url = reverse('received_messages')
        self.response = self.client.get(url)

    def test_messages_received_view_status_code_for_super_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_messages_received_page_template_for_super_users(self):
        self.assertTemplateUsed(self.response, 'messages_received.html')

    def test_messages_received_page_contains_correct_html(self):
        self.assertContains(self.response, 'Jane Doe says "I want to hire you"')

    def test_messages_received_page_url_resolves_pageview(self):
        view = resolve('/message/received')
        self.assertEqual(
            view.func.__name__,
            views.MessagesReceivedView.as_view().__name__
        )


class PastWorksViewTests(TestCase):
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
    def setUp(self):
        url = reverse('new_pastwork')
        self.response = self.client.get(url, follow=True)

    def test_new_pastwork_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 404)


class NewPastWorkViewForSuperUsers(TestCase):
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
    def setUp(self):
        self.past_work = create_pastwork()
        url = reverse('update_pastwork', args=[str(self.past_work.id)])
        self.response = self.client.get(url, follow=True)

    def test_update_pastwork_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 404)


class UpdatePastWorkViewTestsForSuperUsers(TestCase):
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
    def setUp(self):
        self.past_work = create_pastwork()
        url = reverse('delete_pastwork', args=[str(self.past_work.id)])
        self.response = self.client.get(url, follow=True)

    def test_delete_pastwork_view_status_code_for_normal_user(self):
        self.assertEqual(self.response.status_code, 404)


class DeletePastWorkViewTestsForSuperUsers(TestCase):
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