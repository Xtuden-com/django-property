from homes.views import BaseSearchPageView
from homes.forms import SearchForm
from homes_for_sale.models import Sale
from homes_to_let.models import Letting


class AgentBranchHomePageView(BaseSearchPageView):
    template_name="homes-agent/branch.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super(AgentBranchHomePageView, self).get_context_data(**kwargs)
        context['featured'] = {
            'sale': Sale.filtered.published().unexpired().filter(branch__slug=self.kwargs['slug']),
            'letting': Letting.filtered.published().unexpired().filter(branch__slug=self.kwargs['slug'])
        }
        return context