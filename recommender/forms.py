from django import forms

class SongSearchForm(forms.Form):
    song_name = forms.CharField(label='Song Name', max_length=100)
