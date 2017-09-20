from django import forms
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationForm

from .models import PropertyType, SearchPrice

class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['min_price'] = forms.ChoiceField(
            choices=[(o.price, o.label) for o in SearchPrice.objects.all()],
            widget=forms.Select(attrs={'class':'form-control'})
        )
        self.fields['max_price'] = forms.ChoiceField(
            choices=[(o.price, o.label) for o in SearchPrice.objects.all()],
            widget=forms.Select(attrs={'class':'form-control'})
        )

    SEARCH_TYPE_LETTING = 'lettings'
    SEARCH_TYPE_SALE = 'sales'
    SEARCH_TYPE_CHOICES = (
        (SEARCH_TYPE_SALE, 'For Sale'),
        (SEARCH_TYPE_LETTING, 'To Let')
    )
    BEDROOM_CHOICES = (
        (0, 'Studio'),
        (1, '1 Bedroom'),
        (2, '2 Bedrooms'),
        (3, '3 Bedrooms'),
        (4, '4 Bedrooms'),
        (5, '5 Bedrooms+')
    )
    search_type = forms.ChoiceField(choices=SEARCH_TYPE_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    min_price = forms.ChoiceField()
    max_price = forms.ChoiceField()
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    min_bedrooms = forms.ChoiceField(choices=BEDROOM_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    property_type = forms.ModelChoiceField(
        PropertyType.active.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class':'form-control'}),
        to_field_name='slug'
    )


class CustomRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super(CustomRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages = {'required':'Username is required'}
        self.fields['email'].error_messages = {'required':'Email is required'}
        self.fields['password1'].error_messages = {'required':'Password is required'}
        self.fields['password2'].error_messages = {'required':'Password confirmation is required'}


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages = {'required':'Username is required'}
        self.fields['password'].error_messages = {'required':'Password is required'}
