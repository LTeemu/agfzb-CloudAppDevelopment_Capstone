from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    path(route='', view=views.index, name='index'),
    path(route='about', view=views.about, name='about'),
    # path for contact us view
    path(route='contact', view=views.contact, name='contact'),
    # path for registration
    path(route='registration', view=views.registration, name='registration'),

    # path for login
    path(route='login', view=views.login_view, name='login'),

    # path for logout
    path(route='logout', view=views.logout_view, name='logout'),

    path(route='dealers/', view=views.get_dealerships, name='alldealers'),

    path('dealers/<int:dealerId>/',
         views.get_dealerships_by_dealerId, name='index'),

    path('dealers/<str:state>/',
         views.get_dealerships_by_state, name='index'),

    path('dealers/<int:dealerId>/reviews/',
         views.get_reviews_by_dealerId, name='reviews_id'),

    path('dealers/reviews/add/',
         views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
