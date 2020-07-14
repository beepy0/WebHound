from django.shortcuts import render, HttpResponse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from .forms import QueryForm


# Create your views here.
class HoundTrace(FormView):
    template_name = "WebHoundApp/query.html"
    form_class = QueryForm
    success_url = "/webhound/ticket/"

    def form_valid(self, form):
        # call query exec e.g. form.exec_query
        # print(form)
        return HttpResponse(500)

    def form_invalid(self, form):
        # print(form)
        return super().form_invalid(form)


class HoundName(TemplateView):
    template_name = "WebHoundApp/hello.html"
