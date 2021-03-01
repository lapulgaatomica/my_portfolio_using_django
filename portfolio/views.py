from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import About, Competency, Reason, Message


class HomePageView(ListView):
    model = About
    context_object_name = 'abouts'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['competencies'] = Competency.objects.all()
        context['reasons'] = Reason.objects.all()
        return context


class NewAboutView(LoginRequiredMixin, CreateView):
    model = About
    fields = ['paragraph']
    template_name = 'new_aboutme.html'


class UpdateAboutView(LoginRequiredMixin, UpdateView):
    model = About
    fields = ['paragraph']
    template_name = 'update_aboutme.html'


class DeleteAboutView(LoginRequiredMixin, DeleteView):
    model = About
    template_name = 'delete_aboutme.html'
    success_url = reverse_lazy('home')


class NewSkillView(LoginRequiredMixin, CreateView):
    model = Competency
    fields = ['skill']
    template_name = 'new_skill.html'


class UpdateSkillView(LoginRequiredMixin, UpdateView):
    model = Competency
    fields = ['skill']
    template_name = 'update_skill.html'


class DeleteSkillView(LoginRequiredMixin, DeleteView):
    model = Competency
    template_name = 'delete_skill.html'
    success_url = reverse_lazy('home')


class ReasonsView(LoginRequiredMixin, ListView):
    model = Reason
    context_object_name = 'reasons'
    template_name = 'reason.html'


class NewReasonView(LoginRequiredMixin, CreateView):
    model = Reason
    fields = ['purpose']


class UpdateReasonView(LoginRequiredMixin, UpdateView):
    model = Reason
    fields = ['purpose']
    template_name = 'update_reason.html'


class DeleteReasonView(LoginRequiredMixin, DeleteView):
    model = Reason
    template_name = 'delete_reason.html'
    success_url = reverse_lazy('reasons')


class SendMessageView(CreateView):
    model = Message
    fields = ['reason', 'name', 'email', 'message']

    def get_success_url(self):
        # print(self.object.id)
        return reverse('sent_message', kwargs={'pk': self.object.pk})
        # return reverse('reasons')

    def form_valid(self, form):
        subject = 'Message from Portfolio App'
        name_of_sender = form["name"].value()
        reason = Reason.objects.get(id=form["reason"].value()).purpose
        exact_message = form["message"].value()
        sender_email = form["email"].value()
        message = f'{name_of_sender} says {reason}\n\nTheir exact statement was "{exact_message}"\n' \
                  f'Here is their email if you need to reach them: {sender_email}'
        send_mail(subject, message, 'odedoyin25@gmail.com', ['akindeleodedoyin@gmail.com'], fail_silently=False)
        return super(SendMessageView, self).form_valid(form)


class SentMessageView(DetailView):
    model = Message
    context_object_name = 'message'
    template_name = 'message_sent.html'
