from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'password1', 'password2')


class ReviewForm(forms.Form):
    car_make = forms.CharField(label='Car make', max_length=100, required=True)
    car_model = forms.CharField(
        label='Car model', max_length=100, required=True)
    car_year = forms.IntegerField(label='Car year', required=True)
    dealership = forms.IntegerField(label='Dealership ID', required=True)
    id = forms.IntegerField(label='ID', required=True)
    name = forms.CharField(label='Your name', max_length=100, required=True)
    purchase = forms.BooleanField(
        label='Did you make a purchase?', required=False)
    purchase_date = forms.DateField(
        label='Purchase date',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Enter a date in the format YYYY-MM-DD'
    )
    review = forms.CharField(
        label='Your review', widget=forms.Textarea, required=True)
