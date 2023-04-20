import requests
import json
import os
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

COUCH_URL = os.environ.get('COUCH_URL')
IAM_API_KEY = os.environ.get('IAM_API_KEY')
WATSON_URL = os.environ.get('WATSON_URL')
WATSON_API_KEY = os.environ.get('WATSON_API_KEY')

authenticator = IAMAuthenticator(apikey=WATSON_API_KEY)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
)
natural_language_understanding.set_service_url(WATSON_URL)


def get_dealers_from_cf(**kwargs):
    print(f"get_dealers_from_cf kwargs: {kwargs}")
    dealers = []
    response = None

    try:
        print("Fetching url {} ".format(kwargs['url']))
        response = requests.get(kwargs['url'], headers={
                                'Content-Type': 'application/json'}, params=kwargs)

        if response.status_code != 200:
            raise Exception(
                f'Request failed with status code {response.status_code}')

        data = response.json()
        print(f"get_dealers_from_cf dealer json data: {data}")
        if data:
            for dealer in data:
                dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"], id=dealer["id"], lat=dealer["lat"],
                                       long=dealer["long"], short_name=dealer["short_name"], state=dealer["state"], st=dealer["st"], zip=dealer["zip"])
                dealers.append(dealer_obj)
        print(f"get_dealers_from_cf dealer objects: {dealers}")
        return dealers
    except:
        print("Network exception occurred")


def get_dealer_reviews_from_cf(**kwargs):
    print(f"get_dealer_reviews_from_cf kwargs: {kwargs}")
    reviews = []
    response = None

    try:
        print("Fetching url {} ".format(kwargs['url']))
        response = requests.get(kwargs['url'], headers={
                                'Content-Type': 'application/json'}, params=kwargs)

        if response.status_code != 200:
            raise Exception(
                f'Request failed with status code {response.status_code}')

        data = response.json()
        print(f"get_dealer_reviews_from_cf reviews json data: {data}")
        if data:
            for review in data:
                watson_response = response = natural_language_understanding.analyze(
                    text=review['review'],
                    language='en',
                    features=Features(sentiment=SentimentOptions())).get_result()
                # print(watson_response)
                review_obj = DealerReview(
                    id=review['id'],
                    name=review['name'],
                    dealership=review['dealership'],
                    review=review['review'],
                    purchase=review.get('purchase', None),
                    purchase_date=review.get('purchase_date', None),
                    car_make=review.get('car_make', None),
                    car_model=review.get('car_model', None),
                    car_year=review.get('car_year', None),
                    sentiment=watson_response['sentiment']['document']['label']
                )
                reviews.append(review_obj)
        print(f"get_dealer_reviews_from_cf review objects: {reviews}")
        return reviews
    except Exception as error:
        print(f"Error occurred get_dealer_reviews_from_cf: {error}")
