from django.urls import path
from .views import HomePageView, NewAboutView, NewSkillView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('new-aboutme', NewAboutView.as_view(), name='new_about'),
    path('new-skill', NewSkillView.as_view(), name='new_skill'),
]
