from django.urls import path

from .views import HoundTrace, HoundName, HoundDelete

app_name = 'WebHoundApp'
urlpatterns = [
    path('trace/', HoundTrace.as_view(), name='hound_trace'),
    path('deleted/<str:pk>/', HoundDelete.as_view(), name='hound_deleted'),
    path('name/<str:pk>/', HoundName.as_view(), name='hound_name'),
]
