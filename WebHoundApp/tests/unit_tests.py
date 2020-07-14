import os
import django
from django.test import RequestFactory
from rest_framework import status

from ..views import HoundTrace
from ..forms import QueryForm


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebHound.settings")
django.setup()


class RequestSetup:
    def __init__(self, url, request_type, data):
        self.factory = RequestFactory()
        if request_type == 'GET':
            self.request = self.factory.get(url, data=data, content_type='application/json')
        elif request_type == 'POST':
            self.request = self.factory.post(url, data=data, content_type='application/json')


def test_hound_has_trace_method():
    setup = RequestSetup('/webhound/trace/', 'POST', {})
    view = HoundTrace.as_view()

    view(setup.request)


def test_hound_needs_target_query():
    setup = RequestSetup('/webhound/trace/', 'POST', {})
    view = HoundTrace.as_view()

    response = view(setup.request)
    assert response.status_code == status.HTTP_200_OK


def test_hound_gets_target_query():
    form = QueryForm()
    form.declared_fields['query'] = "testUser"
    print(form.declared_fields)
    setup = RequestSetup('/webhound/trace/', 'POST', form)
    view = HoundTrace.as_view()

    response = view(setup.request)

    # print(response)
    assert 0

#
# def test_hound_has_get():
#     assert 0
#
#
# def test_makes_post():
#     assert 0
#
#
# def test_query_saved():
#     assert 0
#
#
# def test_makes_sherlock_call():
#     assert 0
#
#
# def test_query_returns_ticket_nr():
#     assert 0
#
#
# def test_makes_get():
#     assert 0
