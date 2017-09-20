from django.utils.translation import ugettext as _
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
                'required': _('Forename is required'),
            },
            'surname':{
                'required': _('Surname is required'),
            },
            'message':{
                'required': _('Message is required'),
            },
            'telephone':{
                'required': _('Telephone is required'),
            },
            'email':{
                'required': _('Email address is required'),
            },
            'country':{
                'required': _('Country is required'),
            },
            'postcode':{
                'required': _('Postcode is required'),
            },
        }


class LettingDistanceForm(forms.Form):
    distance = forms.ChoiceField(choices=[(10,_('10 Miles')),(20,_('20 Miles'))])
