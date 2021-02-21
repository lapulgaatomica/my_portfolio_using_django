from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView

from .models import About, Competency

class HomePageView(ListView):
    model = About
    context_object_name = 'abouts'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['competencies'] = Competency.objects.all()
        return context

class NewAbout(LoginRequiredMixin, CreateView):
    model = About
    fields = ['paragraph']
    template_name = 'new_aboutme.html'

class NewSkill(LoginRequiredMixin, CreateView):
    model = Competency
    fields = ['skill']
    template_name = 'new_skill.html'
