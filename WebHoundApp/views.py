import csv, os
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from .forms import QueryForm
from .models import Trace
from .serializers import TraceSerializer
from .config import msgs, cfg_data
from .tasks import trace_with_sherlock


# Create your views here.
class HoundTrace(FormView):
    template_name = "WebHoundApp/hound_trace.html"
    form_class = QueryForm

    def form_valid(self, form):
        # call query exec e.g. form.exec_query
        trace_name = form.cleaned_data['query']
        self.success_url = f"/webhound/name/{trace_name}/"

        print(f"receiving trace {trace_name}")
        if Trace.objects.filter(name=trace_name).count() == 0:
            print(f"saving trace {trace_name}")
            Trace(name=trace_name).save()

        trace_with_sherlock.delay(trace_name)
        return super().form_valid(form)


class HoundName(generics.GenericAPIView):
    queryset = Trace.objects.all()
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = TraceSerializer(self.object).data
        if context['was_traced'] is False:
            messages.info(request, msgs['trace_not_done'])
        else:
            try:
                context['results'] = [result for result in context['data'].split(" ; ")][:-2]
            except Exception:
                raise ValueError('was_traced is true but no trace results')
        return Response(template_name="WebHoundApp/hound_name.html", data=context)

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.was_traced is True:
            with open(cfg_data['sherlock_results_dir'].format(self.object.name), newline='') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    self.object.data += f"{str(row[0])} ; "
            self.object.save()

            os.remove(cfg_data['sherlock_results_dir'].format(self.object.name))
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_417_EXPECTATION_FAILED)


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

