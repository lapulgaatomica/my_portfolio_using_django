from django.urls import path
from .views import HomePageView, NewAbout, NewSkill

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('new-aboutme', NewAbout.as_view(), name='new_about'),
    path('new-skill', NewSkill.as_view(), name='new_skill'),
]
