from django.urls import path
from .views import (
    HomePageView,
    NewAboutView,
    UpdateAboutView,
    DeleteAboutView,
    NewSkillView,
    UpdateSkillView,
    DeleteSkillView,
    ReasonsView,
    NewReasonView,
    UpdateReasonView,
    DeleteReasonView,
    SendMessageView,
    SentMessageView,
    MessagesReceivedView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('aboutme/new', NewAboutView.as_view(), name='new_about'),
    path('aboutme/<int:pk>/edit', UpdateAboutView.as_view(), name='edit_about'),
    path('aboutme/<int:pk>/delete', DeleteAboutView.as_view(), name='delete_about'),
    path('skill/new', NewSkillView.as_view(), name='new_skill'),
    path('skill/<int:pk>/edit', UpdateSkillView.as_view(), name='edit_skill'),
    path('skill/<int:pk>/delete', DeleteSkillView.as_view(), name='delete_skill'),
    path('reasons', ReasonsView.as_view(), name='reasons'),
    path('reasons/new', NewReasonView.as_view(), name='new_reason'),
    path('reasons/<int:pk>/edit', UpdateReasonView.as_view(), name='edit_reason'),
    path('reasons/<int:pk>/delete', DeleteReasonView.as_view(), name='delete_reason'),
    path('message/send', SendMessageView.as_view(), name='send_message'),
    path('message/<int:pk>/sent', SentMessageView.as_view(), name='sent_message'),
    path('message/received', MessagesReceivedView.as_view(), name='received_messages')
]
