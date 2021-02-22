from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import About, Competency

class HomePageView(ListView):
    model = About
    context_object_name = 'abouts'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['competencies'] = Competency.objects.all()
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
