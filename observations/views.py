# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin

from .forms import ObservationForm, BatchUploadForm


class AddObservationView(FormView):
    """
    Add a single observation.
    """
    form_class = ObservationForm
    template_name = "observations/add_observation.html"
    success_url = reverse_lazy('observations:add_observation')

    def form_valid(self, form):
        observation = form.save(commit=False)
        observation.observer = self.request.observer
        observation.save()
        return super(AddObservationView, self).form_valid(form)


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
        return super(UploadObservationsView, self).form_valid(form)
