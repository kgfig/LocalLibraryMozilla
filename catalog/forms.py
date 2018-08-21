from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import datetime

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
            widget=forms.SelectDateWidget,
            help_text="Enter a date between now and 4 weeks (default 3 weeks).",
            label='New due date',
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
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
