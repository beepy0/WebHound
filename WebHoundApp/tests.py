"""Generally useful mixins for tests."""
from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse
from django.urls.exceptions import Resolver404

from . import views


class ViewTestMixin(object):
    """Mixin with shortcuts for view tests."""
    longMessage = True  # More verbose error messages
    view_class = None

    def get_view_kwargs(self):
        """
        Returns a dictionary representing the view's kwargs, if necessary.
        If the URL of this view is constructed via kwargs, you can override
        this method and return the proper kwargs for the test.
        """
        return {}

    def get_response(self, method, user, data, args, kwargs):
        """Creates a request and a response object."""
        factory = RequestFactory()
        req_kwargs = {}
        if data:
            req_kwargs.update({'data': data})
        req = getattr(factory, method)('/', **req_kwargs)
        req.user = user if user else AnonymousUser()
        return self.view_class.as_view()(req, *args, **kwargs)

    def is_callable(
        self,
        user=None,
        post=False,
        to=None,
        data={},
        args=[],
        kwargs={},
        status_code=200,
    ):
        """Initiates a call and tests the outcome."""
        view_kwargs = kwargs or self.get_view_kwargs()
        resp = self.get_response(
            'post' if post else 'get',
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

    def is_not_callable(self, **kwargs):
        """Tests if call raises a 404."""
        with self.assertRaises(Http404):
            self.is_callable(**kwargs)

    def is_viewable(
        self,
        url,
        template,
        status_code=200
    ):
        """Makes a get call and verifies the right template is used"""
        resp = self.client.get(reverse(url))
        self.assertEqual(resp.status_code, status_code)
        self.assertTemplateUsed(resp, self.template_path.format(template))


class HoundReleaseTestCase(ViewTestMixin, TestCase):
    view_class = views.HoundTrace
    template_path = 'WebHoundApp/{}.html'

    def test_template(self):
        self.is_viewable(url='WebHoundApp:hound_trace', template='hound_trace')

    def test_get(self):
        self.is_callable()

    def test_post(self):
        self.is_callable(post=True)

    def test_post_no_data(self):
        self.is_callable(post=True, data={'query': ''}, status_code=200)

    def test_post_with_data(self):
        self.is_callable(post=True, data={'query': 'dummy_name'}, to='hound_name')


class HoundCallBackTestCase(ViewTestMixin, TestCase):
    view_class = views.HoundName
