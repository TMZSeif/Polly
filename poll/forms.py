from django import forms

class PollForm(forms.Form):
    question = forms.CharField(max_length=100)

class OptionForm(forms.Form):
    name = forms.CharField(max_length=100)