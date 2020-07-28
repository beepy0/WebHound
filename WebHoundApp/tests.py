import pytz
from datetime import datetime, timedelta
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse
from django.urls.exceptions import Resolver404
from django.shortcuts import Http404
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

from . import views
from .models import Trace, Counter
from .tasks import trace_with_sherlock
from .config import errors, cfg_data


class ViewTestMixin(object):
    """Mixin with shortcuts for view tests."""
    longMessage = True  # More verbose error messages
    view_class = None

    def annotate_req(self, req):
        """Annotate a request object with a session"""
        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()

        """Annotate a request object with a messages"""
        middleware = MessageMiddleware()
        middleware.process_request(req)
        req.session.save()

    def get_view_kwargs(self):
        """
        Returns a dictionary representing the view's kwargs, if necessary.
        If the URL of this view is constructed via kwargs, you can override
        this method and return the proper kwargs for the test.
        """
        return {}

    def get_response(self, req, anno, user, data, args, kwargs):
        """Creates a request and a response object."""
        factory = RequestFactory()
        req_kwargs = {}
        if data:
            req_kwargs.update({'data': data})
        req = getattr(factory, req)('/', **req_kwargs)
        # requests that use messages need extra annotation
        if anno is True:
            self.annotate_req(req)
        req.user = user if user else AnonymousUser()
        return self.view_class.as_view()(req, *args, **kwargs)

    def is_callable(
        self,
        user=None,
        req=None,
        anno=False,
        to=None,
        data={},
        args=[],
        kwargs={},
        template=None,
        route=None,
        status_code=200,
    ):
        """Initiates a call and tests the outcome."""
        view_kwargs = kwargs or self.get_view_kwargs()
        resp = self.get_response(
            req if req else 'get',
            anno,
            user=user,
            data=data,
            args=args,
            kwargs=view_kwargs,
        )
        if to:
            self.assertIn(resp.status_code, [301, 302],
                          msg='The request was not redirected.')
            try:
                self.assertEqual(
                    resolve(resp.url.split('?')[0].split('#')[0]).url_name, to,
                    msg='Should redirect to "{}".'.format(to))
            except Resolver404:
                raise Exception('Could not resolve "{}".'.format(resp.url))
        else:
            self.assertEqual(resp.status_code, status_code)
        if template:
            # resp.url is only given on a redirect, otherwise it has to be constructed
            url = resp.url if to else reverse(f"{self.app_name}:{route}", kwargs=kwargs)
            self.is_viewable(url, template)

    def is_viewable(
        self,
        url,
        template
    ):
        """Makes a get call and verifies the right template is used"""
        self.assertTemplateUsed(self.client.get(url), f"{self.app_name}/{template}.html")


class HoundTraceTestCase(ViewTestMixin, TestCase):
    view_class = views.HoundTrace
    app_name = 'WebHoundApp'

    def setUp(self):
        Counter(id='traces').save()

    def test_get(self):
        self.is_callable()

    def test_get_template(self):
        self.is_callable(template='hound_trace', route='hound_trace')

    def test_get_no_counter(self):
        Counter.objects.get(id='traces').delete()
        with self.assertRaisesMessage(Http404, errors['no_cnt_instance']):
            self.is_callable()

    def test_post(self):
        self.is_callable(req='post')

    def test_post_template(self):
        self.is_callable(req='post', template='hound_trace', route='hound_trace')

    def test_post_no_data(self):
        self.is_callable(req='post', data={'query': ''}, template='hound_trace', route='hound_trace',
                         status_code=200)

    def test_post_with_data(self):
        self.is_callable(req='post', data={'query': 'dummy_name'}, to='hound_name', template='hound_name')


class HoundQueryTestCase(ViewTestMixin, TestCase):
    view_class = views.HoundName
    app_name = 'WebHoundApp'

    def test_get_traced(self):
        name = 'user123'
        self.is_callable(req='get', anno=True, status_code=404, kwargs={'pk': 'no_such_user'})
        # simulates the celery task success result
        Trace(name=name, was_traced=True, data="url1 ; url2 ; url3 ; misc ; ").save()

        self.is_callable(req='get', anno=True, kwargs={'pk': name}, template='hound_name', route='hound_name')

        resp = self.get_response(req='get', anno=True, user=None, data={}, args=[], kwargs={'pk': name})
        self.assertEqual(resp.data['results'], ['url1', 'url2', 'url3'])

    def test_get_traced_but_no_data(self):
        name = 'user123'
        Trace(name=name, was_traced=True).save()

        with self.assertRaisesMessage(ValueError, errors['was_traced_no_data']):
            self.get_response(req='get', anno=True, user=None, data={}, args=[], kwargs={'pk': name})

    def test_get_not_traced(self):
        name = 'user123'
        Trace(name=name, was_traced=False).save()
        resp = self.get_response(req='get', anno=True, user=None, data={}, args=[], kwargs={'pk': name})

        self.assertEqual(resp.data.get('results', ""), "")

    def test_post(self):
        Trace(name='dummy_user').save()
        self.is_callable(req='post', status_code=405, kwargs={'pk': 'dummy_user'})

    # TODO test retry trace here
    def test_put(self):
        name = 'user123'
        Trace(name=name, was_traced=False).save()
        trace = Trace.objects.get(name=name)

        self.is_callable(req='put', kwargs={'pk': name}, route='hound_name')

        trace.was_traced = True
        trace.save()

        self.is_callable(req='put', kwargs={'pk': name}, route='hound_name')


class HoundDeleteTestCase(ViewTestMixin, TestCase):
    view_class = views.HoundDelete
    app_name = 'WebHoundApp'

    def setUp(self):
        # redirects to the main page will also need a Counter instance for the template
        Counter(id='traces').save()

    def test_delete(self):
        name = 'user123'
        Trace(name=name).save()
        self.is_callable(req='post', kwargs={'pk': name}, to='hound_trace', template='hound_trace')


class SherlockTaskTestCase(TestCase):
    def test_no_trace(self):
        with self.assertRaisesMessage(KeyError, expected_message=errors['no_name_in_db']):
            trace_with_sherlock('no_such_name')

    def test_trace_done(self):
        Trace(name='sample_trace', was_traced=True).save()
        self.assertIs(trace_with_sherlock('sample_trace'), True)

    def test_trace_done_bad_ts(self):
        Trace(name='sample_trace', was_traced=True,
              task_active_ts=cfg_data['default_task_ts'] - timedelta(hours=1)).save()
        self.assertRaisesMessage(ValueError, errors['no_task_ts'])

    def test_trace_duplicate_slow_or_crashed(self):
        name = 'sample_trace'
        ts_reference = datetime.now(tz=pytz.utc)
        Trace(name=name, was_traced=False, task_active_ts=ts_reference - timedelta(minutes=11)).save()
        trace_with_sherlock(name)
        trace = Trace.objects.get(pk=name)
        self.assertNotEquals(trace.task_active_ts, ts_reference)

    def test_trace_duplicate_active(self):
        name = 'sample_trace'
        Trace(name=name, was_traced=False, task_active_ts=datetime.now(tz=pytz.utc)).save()
        trace_with_sherlock(name)
        self.assertIs(trace_with_sherlock(name), True)
