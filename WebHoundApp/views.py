from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.contrib import messages
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .forms import QueryForm
from .models import Trace
from .serializers import TraceSerializer
from .config import msgs


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
        trace = TraceSerializer(self.object)
        if trace.data['was_traced'] is False:
            messages.info(request, msgs['trace_not_done'])
        return Response(template_name="WebHoundApp/hound_name.html", data=trace.data)

    def delete(self, request, *args, **kwargs):
        # self.lookup_field = 'name'
        get_object_or_404(self.queryset, pk=kwargs['pk']).delete()
        return HttpResponseRedirect(reverse('WebHoundApp:hound_deleted', kwargs={'pk': kwargs['pk']}))


class HoundDelete(View):

    def get(self, request, *args, **kwargs):
        if kwargs == {}:
            raise Http404('No trace name supplied')
        return render(request, 'WebHoundApp/hound_deleted.html', context=kwargs)