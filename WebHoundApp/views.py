from django.urls import reverse_lazy
from django.views.generic.edit import FormView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .forms import QueryForm
from .models import Trace
from .serializers import TraceSerializer
from .config import msgs
from .tasks import trace_with_sherlock


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

        trace_with_sherlock.delay(trace_name)
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

    def put(self, request, *args, **kwargs):
        # collect data
        # store data
        # delete csv and txt files

        self.object = self.get_object()
        self.object.data = request.PUT['data']
        self.object.save()
        return Response(status=status.HTTP_200_OK)


class HoundDelete(DeleteView):
    model = Trace
    template_name = 'WebHoundApp/hound_delete.html'

    def get_context_data(self, **kwargs):
        context = super(HoundDelete, self).get_context_data(**kwargs)
        context['pk'] = self.request.GET['pk']
        return context

    def get_success_url(self):
        trace_name = self.kwargs['pk']
        return reverse_lazy('WebHoundApp:hound_deleted', kwargs={'pk': trace_name})


class HoundDeleted(TemplateView):
    template_name = 'WebHoundApp/hound_deleted.html'

