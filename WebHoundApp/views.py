import os
from django.shortcuts import render, HttpResponse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from .forms import QueryForm


# Create your views here.
class HoundTrace(FormView):
    template_name = "WebHoundApp/hound_trace.html"
    form_class = QueryForm
    success_url = "/webhound/name/"

    def form_valid(self, form):
        # call query exec e.g. form.exec_query
        # create new trace entry
        # -
        os.system('ls')
        return super().form_valid(form)


class HoundName(TemplateView):
    template_name = "WebHoundApp/hound_name.html"
