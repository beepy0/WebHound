from django.urls import path

from django.conf import settings
from django.views.decorators.cache import cache_control
from django.contrib.staticfiles.views import serve
from django.conf.urls.static import static

from .views import HoundTrace, HoundName, HoundDelete

app_name = 'WebHoundApp'
urlpatterns = [
    path('trace/', HoundTrace.as_view(), name='hound_trace'),
    path('delete/<str:pk>/', HoundDelete.as_view(), name='hound_delete'),
    path('name/<str:pk>/', HoundName.as_view(), name='hound_name'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, view=cache_control(no_cache=True, must_revalidate=True)(serve))
