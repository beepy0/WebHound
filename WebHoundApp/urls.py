from django.urls import path

from .views import HoundTrace, HoundName, HoundDelete, HoundDeleted

app_name = 'WebHoundApp'
urlpatterns = [
    path('trace/', HoundTrace.as_view(), name='hound_trace'),
    path('delete/<str:pk>/', HoundDelete.as_view(), name='hound_delete'),
    path('deleted/<str:pk>/', HoundDeleted.as_view(), name='hound_deleted'),
    path('name/<str:pk>/', HoundName.as_view(), name='hound_name'),
]
