from django import forms

class BandSearchForm(forms.Form):
    band_name = forms.CharField(label='Artist Name', max_length=100)
