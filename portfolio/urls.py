from django.urls import path
from .views import (
    HomePageView,
    NewAboutView,
    UpdateAboutView,
    DeleteAboutView,
    NewSkillView,
    UpdateSkillView,
    DeleteSkillView
    )

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('aboutme/new', NewAboutView.as_view(), name='new_about'),
    path('aboutme/<int:pk>/edit', UpdateAboutView.as_view(), name='edit_about'),
    path('aboutme/<int:pk>/delete', DeleteAboutView.as_view(), name='delete_about'),
    path('skill/new', NewSkillView.as_view(), name='new_skill'),
    path('skill/<int:pk>/edit', UpdateSkillView.as_view(), name='edit_competency'),
    path('skill/<int:pk>/delete', DeleteSkillView.as_view(), name='delete_competency'),
]
