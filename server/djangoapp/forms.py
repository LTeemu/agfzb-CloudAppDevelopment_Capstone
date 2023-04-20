from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CarModel
import uuid


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'password1', 'password2')


class ReviewForm(forms.Form):
    # car_make = forms.CharField(label='Car make', max_length=100, required=True)
    # car_model = forms.CharField(label='Car model', max_length=100, required=True)
    # car_year = forms.IntegerField(label='Car year', required=True)

    dealership = forms.IntegerField(
        label='Dealership ID', widget=forms.HiddenInput())

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='id')
    id = forms.IntegerField(widget=forms.HiddenInput())

    name = forms.CharField(widget=forms.HiddenInput(), max_length=100)

    purchase = forms.BooleanField(
        label='Bought car from this dealer?', required=False)

    car = forms.ModelChoiceField(
        label='Select car', queryset=CarModel.objects.all(), required=False)

    purchase_date = forms.DateField(
        label='Purchase date',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    review = forms.CharField(
        label='Your review', widget=forms.Textarea, required=True)
