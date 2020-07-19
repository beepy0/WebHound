from rest_framework import serializers
from .models import Trace


class TraceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trace
        fields = ['date', 'was_traced', 'name', 'data']
