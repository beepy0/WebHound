from django.urls import reverse_lazy
from django.views.generic.edit import FormView, DeleteView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from .forms import QueryForm
from .models import Trace, Counter
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

    def get_context_data(self, **kwargs):
        context = super(HoundTrace, self).get_context_data(**kwargs)
        context['traces_cnt'] = get_object_or_404(Counter, id='traces_all').count
        return context


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
                context['results'] = context['data'][:-2]
            except Exception:
                raise ValueError('was_traced is true but no trace results')
        return Response(template_name="WebHoundApp/hound_name.html", data=context)

    def put(self, request, *args, **kwargs):
        # reserve for retry feature
        ...


class HoundDelete(DeleteView):
    model = Trace

    def get_success_url(self):
        return reverse_lazy('WebHoundApp:hound_trace')
