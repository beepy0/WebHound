"""Generally useful mixins for tests."""
from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse
from django.urls.exceptions import Resolver404
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

from . import views
from .models import Trace


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

    def get_response(self, method, anno, user, data, args, kwargs):
        """Creates a request and a response object."""
        factory = RequestFactory()
        req_kwargs = {}
        if data:
            req_kwargs.update({'data': data})
        req = getattr(factory, method)('/', **req_kwargs)
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

    def is_not_callable(self, **kwargs):
        """Tests if call raises a 404."""
        with self.assertRaises(Http404):
            self.is_callable(**kwargs)

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

    def test_get(self):
        self.is_callable()

    def test_get_template(self):
        self.is_callable(template='hound_trace', route='hound_trace')

    def test_post(self):
        self.is_callable(req='post')

    def test_post_template(self):
        self.is_callable(req='post', template='hound_trace', route='hound_trace')

    def test_post_no_data(self):
        self.is_callable(req='post', data={'query': ''}, template='hound_trace', route='hound_trace',
                         status_code=200)

    def test_post_with_data(self):
        self.is_callable(req='post', data={'query': 'dummy_name'}, to='hound_name',
                         template='hound_name', route='hound_trace')


class HoundCallBackTestCase(ViewTestMixin, TestCase):
    view_class = views.HoundName
    app_name = 'WebHoundApp'
    # initializing this way gets rid of the route parameter but can add redundancy
    # if we need to change the route in a specific test
    # class_url = reverse(f"{app_name}:hound_name", kwargs={'pk': 'tmp'}).split('tmp')[0]

    def test_get(self):
        self.is_callable(req='get', anno=True, status_code=404, kwargs={'pk': 'no_such_user'})
        Trace(name='dummy_user').save()
        self.is_callable(req='get', anno=True, kwargs={'pk': 'dummy_user'}, template='hound_name', route='hound_name')

    def test_post(self):
        Trace(name='dummy_user').save()
        self.is_callable(req='post', status_code=405, kwargs={'pk': 'dummy_user'})

    # TODO test retry trace here
    def test_put(self):
        Trace(name='dummy_user').save()
        self.is_callable(req='put', status_code=405, kwargs={'pk': 'dummy_user'})

    def test_delete(self):
        Trace(name='dummy_user').save()
        self.is_callable(req='get', anno=True, kwargs={'pk': 'dummy_user'}, template='hound_name', route='hound_name')
        self.is_callable(req='delete', kwargs={'pk': 'dummy_user'},
                         to='hound_deleted', template='hound_deleted', route='hound_deleted')
        self.is_callable(req='get', anno=True, status_code=404, kwargs={'pk': 'dummy_user'})


class HoundDeleteTestCase(ViewTestMixin, TestCase):
    view_class = views.HoundDelete
    app_name = 'WebHoundApp'

    def test_get(self):
        self.is_callable(req='get', kwargs={'pk': 'deleted_dummy_user'},
                         template='hound_deleted', route='hound_deleted')

    def test_get_no_data(self):
        with self.assertRaises(Http404, msg='No trace name supplied'):
            self.is_callable(req='get')


# class SherlockTaskTestCase(TestCase):
#     def test_no_trace(self):
#         # check if object exists
#         # if not, raise NoObjectException
#         assert 0
#
#     def test_trace_proper(self):
#         assert 0
#
#     def test_trace_duplicate(self):
#         # a task queries object and checks "is_task_active"
#         # if yes, it checks if "task_active_date" is older than 10 minutes
#         # if no, it is a duplicate -> complete task
#         # if yes, previous task likely crashed -> take over trace and update "task_active_date"
#         assert 0
#
#     def test_trace_already_done(self):
#         assert 0
