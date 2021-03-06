from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

from .models import CarMake, CarModel, CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_by_state_from_cf, get_dealer_reviews_from_cf, post_request

from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/user_registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://b8d6e378.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Get dealers from the URL and state
        #dealerships = get_dealer_by_state_from_cf(url, "VA")

        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        # For debugging
        # return HttpResponse(dealer_names)

        context["dealership_list"] = dealerships

        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://b8d6e378.eu-gb.apigw.appdomain.cloud/api/review"
        # Get dealer reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        #reviews = get_dealer_reviews_from_cf(url, "15")

        # Concat all dealer's short name
        reviews_names = ' '.join([review.sentiment for review in reviews])
        # Return a list of dealer short name
        #return HttpResponse(reviews_names)

        context["dealership_reviews"] = reviews
        context["dealer_id"] = dealer_id

        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    #if request.user.is_authenticated():
    context = {}
    if request.method == "GET":
        cars = CarModel.objects.all()

        context["dealer_id"] = dealer_id
        context["cars"] = cars

        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":

        url = "https://b8d6e378.eu-gb.apigw.appdomain.cloud/api/review"

        review = dict()
        review["dealership"] = dealer_id
        #review["review"] = request.POST['review']
        review["review"] = request.POST.get('review', " ")
        review["name"] = request.user.first_name + " " + request.user.last_name
 
        if request.POST.get('purchasecheck', False):
            review["purchase"] = True
        else:
            review["purchase"] = False

        review["purchase_date"] = request.POST.get('purchasedate', datetime.utcnow().isoformat())

        #if request.POST['purchasedate']:
        #    review["purchase_date"] = request.POST['purchasedate']
        #else:
        #    review["purchase_date"] = datetime.utcnow().isoformat()

        car = get_object_or_404(CarModel, pk=request.POST['car'])

        review["car_make"] = car.carmake.name
        review["car_model"] = car.name
        review["car_year"] = car.year.strftime("%Y")

        json_payload  = dict()
        json_payload = review
        #json_payload["review"] = review

        json_result = post_request(url, json_payload, dealerId=dealer_id)

        print(json_result)
        #return HttpResponse(json_result)
        return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
        