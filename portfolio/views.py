from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import About, Competency, Reason

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

class NewReasonView(LoginRequiredMixin, CreateView):
    model = Reason
    fields = ['purpose']

class ReasonsView(LoginRequiredMixin, ListView):
    model = Reason
    context_object_name = 'reasons'
    template_name = 'reason.html'

class UpdateReasonView(LoginRequiredMixin, UpdateView):
    model = Reason
    fields = ['purpose']
    template_name = 'update_reason.html'

class DeleteReasonView(LoginRequiredMixin, DeleteView):
    model = Reason
    template_name = 'delete_reason.html'
    success_url = reverse_lazy('reasons')
