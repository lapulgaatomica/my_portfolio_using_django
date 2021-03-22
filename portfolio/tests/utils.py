from django.contrib.auth import get_user_model
from ..models import PastWork


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