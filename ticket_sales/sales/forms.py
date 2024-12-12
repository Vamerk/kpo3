from django import forms

class TicketPurchaseForm(forms.Form):
    full_name = forms.CharField(max_length=200)
    passport_series = forms.CharField(max_length=10)
    passport_number = forms.CharField(max_length=10)