from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, ListView

from braces.views import LoginRequiredMixin

from .forms import ObservationForm, BatchUploadForm
from .models import Observation
from observers.models import Observer
from stars.models import Star


class ObservationListView(ListView):
    queryset = Observation.objects.all()
    template_name = "observations/observation_list.html"

    def get_queryset(self):
        queryset = super().get_queryset().select_related('star', 'observer', 'observer__user')
        if not self.kwargs.get('observer_id'):
            return queryset
        return queryset.filter(observer_id=self.kwargs['observer_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.kwargs.get('observer_id'):
            return context
        context['observer'] = get_object_or_404(Observer, pk=self.kwargs['observer_id'])
        return context


class AddObservationView(LoginRequiredMixin, FormView):
    """
    Add a single observation.
    """
    form_class = ObservationForm
    template_name = "observations/add_observation.html"
    success_url = reverse_lazy('observations:add_observation')

    def get_initial(self):
        star_id = self.kwargs.get('star_id')
        if star_id:
            return {
                'star': get_object_or_404(Star, pk=star_id),
            }
        else:
            return {}

    def form_valid(self, form):
        observation = form.save(commit=False)
        observation.observer = self.request.observer
        observation.save()
        messages.success(self.request, _("Observation added successfully!"))
        return super().form_valid(form)


class UploadObservationsView(LoginRequiredMixin, FormView):
    """
    Upload a file of observations.
    """
    form_class = BatchUploadForm
    template_name = "observations/upload_observations.html"
    success_url = reverse_lazy('observations:upload_observations')

    def form_valid(self, form):
        form.process_file()
        messages.success(self.request, _("File uploaded successfully!"))
        return super().form_valid(form)
