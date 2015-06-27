from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Observer


class ObserverForm(forms.ModelForm):
    first_name = forms.CharField(label=_("First name"), max_length=30, required=False)
    last_name = forms.CharField(label=_("Last name"), max_length=30, required=False)

    class Meta:
        model = Observer
        fields = ['first_name', 'last_name', 'aavso_code', 'limiting_magnitude', 'location', 'city']

    def __init__(self, *args, **kwargs):
        super(ObserverForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, *args, **kwargs):
        observer = super(ObserverForm, self).save(*args, **kwargs)
        observer.user.first_name = self.cleaned_data.get('first_name')
        observer.user.last_name = self.cleaned_data.get('last_name')
        observer.user.save()
        return observer
