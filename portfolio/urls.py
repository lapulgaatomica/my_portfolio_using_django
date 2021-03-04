from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('aboutme/new', views.NewAboutView.as_view(), name='new_about'),
    path('aboutme/<int:pk>/edit', views.UpdateAboutView.as_view(), name='edit_about'),
    path('aboutme/<int:pk>/delete', views.DeleteAboutView.as_view(), name='delete_about'),
    path('skill/new', views.NewSkillView.as_view(), name='new_skill'),
    path('skill/<int:pk>/edit', views.UpdateSkillView.as_view(), name='edit_skill'),
    path('skill/<int:pk>/delete', views.DeleteSkillView.as_view(), name='delete_skill'),
    path('reasons', views.ReasonsView.as_view(), name='reasons'),
    path('reasons/new', views.NewReasonView.as_view(), name='new_reason'),
    path('reasons/<int:pk>/edit', views.UpdateReasonView.as_view(), name='edit_reason'),
    path('reasons/<int:pk>/delete', views.DeleteReasonView.as_view(), name='delete_reason'),
    path('message/send', views.SendMessageView.as_view(), name='send_message'),
    path('message/received', views.MessagesReceivedView.as_view(), name='received_messages'),
    path('pastworks', views.PastWorksView.as_view(), name='pastworks'),
    path('pastwork/new', views.NewPastWorkView.as_view(), name='new_pastwork'),
    path('pastwork/<int:pk>', views.PastWorkView.as_view(), name='pastwork'),
    path('pastwork/<int:pk>/edit', views.UpdatePastWorkView.as_view(), name='update_pastwork'),
    path('pastwork/<int:pk>/delete', views.DeletePastWorkView.as_view(), name='delete_pastwork'),
]
