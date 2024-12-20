from django import forms
from .models import TransportType, Ticket


class TicketPurchaseForm(forms.Form):
    full_name = forms.CharField(max_length=200)
    passport_series = forms.CharField(max_length=10)
    passport_number = forms.CharField(max_length=10)


class TicketFilterForm(forms.Form):
    transport_type = forms.ModelChoiceField(
        queryset=TransportType.objects.all(),
        required=False,
        label="Тип транспорта"
    )
    start_date = forms.DateTimeField(
        required=False,
        label="Дата начала",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    end_date = forms.DateTimeField(
        required=False,
        label="Дата окончания",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )