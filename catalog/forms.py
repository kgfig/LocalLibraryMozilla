from django.forms import ModelForm, SelectDateWidget
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import datetime

from catalog.models import BookInstance

class RenewBookModelForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {
            'due_back': _('Renewal date'),
        }
        help_texts = {
            'due_back': _('Enter a date between today and 4 weeks from now.'),
        }
        widgets = {
            'due_back': SelectDateWidget,
        }

    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        date_today = datetime.date.today()

        # Check if date is not in the past
        if data < date_today:
            raise ValidationError(
                _('Invalid date %(value)s. Set date in the future up to 4 weeks from today.'),
                code='invalid',
                params={'value': data},
            )

        # Check if date is in the allowed range (4 weeks from today)
        if data > date_today + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date %(value)s. Choose a date no further than 4 weeks from today.'),
                code='invalid',
                params={'value':data},
            )

        return data
