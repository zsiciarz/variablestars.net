from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin

from .forms import ObservationForm, BatchUploadForm
from stars.models import Star


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
