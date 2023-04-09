from django import forms
from base.models import *

class Search(forms.Form):
    searchtext = forms.CharField(max_length=100, label='', required=False)

class TicketEd(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'message']
        # exclude = ['profile', 'created_at']
