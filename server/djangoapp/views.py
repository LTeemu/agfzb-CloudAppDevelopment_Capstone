import logging
import json
import requests
import os
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .forms import CustomUserCreationForm, ReviewForm
from urllib.parse import urlencode
from django.views.decorators.http import require_http_methods
import uuid
from .models import CarMake

# Get an instance of a logger
logger = logging.getLogger(__name__)

COUCH_URL = os.environ.get('COUCH_URL')
IAM_API_KEY = os.environ.get('IAM_API_KEY')
GET_DEALERSHIP_URL = os.environ.get('GET_DEALERSHIP_URL')
GET_REVIEWS_URL = os.environ.get('GET_REVIEWS_URL')
POST_REVIEW_URL = os.environ.get('POST_REVIEW_URL')
# Create your views here.
# Create an `about` view to render a static about page


def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page


def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

# Create a `login` view to handle sign in request


def index(request):
    if request.method == "GET":
        return render(request, 'djangoapp/index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return redirect('djangoapp:index')

# Create a `logout` view to handle sign out request


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request


def registration(request):
    context = {}
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            print(form.errors)
            context['form'] = form
            return render(request, 'djangoapp/registration.html', context)
    else:
        return render(request, 'djangoapp/registration.html', context)
# Update the `get_dealerships` view to render the index page with a list of dealerships


@require_http_methods(["GET"])
def get_dealerships(request):
    context = {}
    kwargs = {'url': GET_DEALERSHIP_URL, 'COUCH_URL': COUCH_URL,
              'IAM_API_KEY': IAM_API_KEY}
    dealerships = get_dealers_from_cf(**kwargs)
    print(f"get_dealerships result: {dealerships}")
    context["dealerships"] = dealerships
    return render(request, 'djangoapp/index.html', context)


@require_http_methods(["GET"])
def get_dealerships_by_state(request, state):
    if state:
        context = {}
        query_string = urlencode({'state': state})
        url = f"{GET_DEALERSHIP_URL}?{query_string}"
        kwargs = {'url': url, 'COUCH_URL': COUCH_URL,
                  'IAM_API_KEY': IAM_API_KEY, 'state': state}
        dealerships = get_dealers_from_cf(**kwargs)
        print(f"get_dealerships_by_state result: {dealerships}")
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)


@require_http_methods(["GET"])
def get_dealerships_by_dealerId(request, dealerId):
    if dealerId:
        context = {}
        query_string = urlencode({'dealerId': dealerId})
        url = f"{GET_DEALERSHIP_URL}?{query_string}"
        kwargs = {'url': url, 'COUCH_URL': COUCH_URL,
                  'IAM_API_KEY': IAM_API_KEY, 'dealerId': dealerId}
        dealerships = get_dealers_from_cf(**kwargs)
        print(f"get_dealerships_by_dealerId result: {dealerships}")
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
@require_http_methods(["GET"])
def get_reviews_by_dealerId(request, dealerId):
    if dealerId:
        context = {'dealerId': dealerId}
        query_string = urlencode({'dealerId': dealerId})
        url = f"{GET_REVIEWS_URL}?{query_string}"
        kwargs = {'url': url, 'COUCH_URL': COUCH_URL,
                  'IAM_API_KEY': IAM_API_KEY, 'dealerId': dealerId}
        reviews = get_dealer_reviews_from_cf(**kwargs)
        print(f"get_dealer_reviews_from_cf result: {reviews}")
        context["reviews"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review


def add_review(request, dealerId):
    context = {'dealerId': dealerId}
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():

            if form.cleaned_data['purchase']:
                purchase_date = form.cleaned_data['purchase_date']
                form.cleaned_data['purchase_date'] = purchase_date.strftime(
                    '%d/%m/%Y')
                car = form.cleaned_data['car']
                print(f"car vars {vars(car)}")
                form.cleaned_data['car_make'] = car.make.name
                form.cleaned_data['car_model'] = car.name
                form.cleaned_data['car_year'] = car.year.year
                del form.cleaned_data['car']
            print(f"form post data: {form.cleaned_data}")
            data = {
                'COUCH_URL': COUCH_URL,
                'IAM_API_KEY': IAM_API_KEY,
                'dealerId': form.cleaned_data['id'],
                'review': form.cleaned_data
            }
            response = requests.post(POST_REVIEW_URL, json=data)
            print(f"response post: {response.json()}")
            print(f"response status: {response}")
            if response.status_code == 201:
                return redirect('djangoapp:reviews_id', dealerId)
        else:
            print(f'post invalid with values {form.cleaned_data}')
            # Handle form validation errors here
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")
    else:
        uuid_str_without_hyphens = str(uuid.uuid4()).replace('-', '')
        uuid_int = int(uuid_str_without_hyphens, 16)
        context['form'] = ReviewForm(
            initial={
                'dealership': dealerId,
                'name': ' '.join([request.user.first_name, request.user.last_name]),
                'id': uuid_int
            }
        )
        print(f"Context from view {context['form'].initial}")
        return render(request, 'djangoapp/add_review.html', context)
