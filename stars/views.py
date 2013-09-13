from __future__ import unicode_literals

from django.views.generic import ListView, DetailView

from .models import Star


class StarListView(ListView):
    """
    Display a list of variable stars.
    """
    model = Star
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(StarListView, self).get_context_data(**kwargs)
        context['total_star_count'] = Star.objects.count()
        return context


class StarSearchView(ListView):
    """
    Display a list of all stars matching submitted query.
    """
    model = Star
    paginate_by = 20
    template_name = "stars/star_search.html"

    def get_queryset(self):
        q = self.request.REQUEST.get('q')
        return Star.objects.filter(name__icontains=q)


class StarDetailView(DetailView):
    """
    Detailed information about a variable star.
    """
    model = Star
