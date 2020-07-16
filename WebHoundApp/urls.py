from django.urls import path

from .views import HoundTrace, HoundName

app_name = 'WebHoundApp'
urlpatterns = [
    path('trace/', HoundTrace.as_view(), name='hound_trace'),
    path('name/<str:pk>/', HoundName.as_view(), name='hound_name'),
]