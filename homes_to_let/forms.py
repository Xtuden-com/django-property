from django.forms import ModelForm, Textarea, TextInput, EmailInput, CheckboxInput
from django import forms
from .models import LettingContact

class LettingContactForm(ModelForm):
    class Meta:
        model = LettingContact
        fields = [
            'more_details','view_property','title','forename','surname',
            'message','telephone','email','country','postcode'
        ]
        widgets = {
            'forename': TextInput(attrs={'class':'form-control'}),
            'surname': TextInput(attrs={'class':'form-control'}),
            'message': Textarea(attrs={'cols':10,'rows':5,'class':'form-control'}),
            'telephone': TextInput(attrs={'class':'form-control'}),
            'email': EmailInput(attrs={'class':'form-control'}),
            'country': TextInput(attrs={'class':'form-control'}),
            'postcode': TextInput(attrs={'class':'form-control'}),
            'more_details': CheckboxInput(attrs={'class':'custom-control-input'}),
            'view_property': CheckboxInput(attrs={'class':'custom-control-input'})
        }
        error_messages = {
            'forename':{
                'required': 'Forename is required',
            },
            'surname':{
                'required': 'Surname is required',
            },
            'message':{
                'required': 'Message is required',
            },
            'telephone':{
                'required': 'Telephone is required',
            },
            'email':{
                'required': 'Email address is required',
            },
            'country':{
                'required': 'Country is required',
            },
            'postcode':{
                'required': 'Postcode is required',
            },
        }

class LettingDistanceForm(forms.Form):
    distance = forms.ChoiceField(choices=[(10,'10 Miles'),(20,'20 Miles')])
