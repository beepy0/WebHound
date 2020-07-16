import os
from django.shortcuts import render, HttpResponse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .forms import QueryForm
from .models import Trace


# Create your views here.
class HoundTrace(FormView):
    template_name = "WebHoundApp/hound_trace.html"
    form_class = QueryForm

    def form_valid(self, form):
        # call query exec e.g. form.exec_query
        trace_name = form.cleaned_data['query']
        self.success_url = f"/webhound/name/{trace_name}/"

        if Trace.objects.filter(name=trace_name).count() == 0:
            Trace(name=trace_name).save()

        # TODO os.system(f"python WebHoundApp\\sherlock\\sherlock -o WebHoundApp\\sherlock\\results\\{trace_name}.csv --csv --print-found {trace_name}")
        return super().form_valid(form)


class HoundName(generics.GenericAPIView):
    queryset = Trace.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response(template_name="WebHoundApp/hound_name.html")