from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin, GroupRequiredMixin

class AgentHomePageView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = "homes-agent-home.html"
    group_required = "agent"