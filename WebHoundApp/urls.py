from django.urls import path

from .views import HoundTrace, HoundName

app_name = 'WebHoundApp'
urlpatterns = [
    path('trace/', HoundTrace.as_view(), name='release_hound'),
    path('ticket/', HoundName.as_view(), name='name_hound'),
]