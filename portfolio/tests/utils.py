from django.contrib.auth import get_user_model
from ..models import PastWork, Reason, Message, Competency, About


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


def create_reason():
    return Reason.objects.create(purpose='I want to hire you')


def create_message():
    reason = create_reason()
    return Message.objects.create(reason=reason, name='Jane Doe', email='jane@doe.com', message='Hey Dele')


def create_skill():
    return Competency.objects.create(skill='Development and Source Control (Docker, Git, Github)')


def create_about():
    return About.objects.create(paragraph='I am a backend developer')