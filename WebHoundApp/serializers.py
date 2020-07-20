from rest_framework import serializers
from .models import Trace


class TraceSerializer(serializers.ModelSerializer):
    date_friendly = serializers.DateTimeField(source='date', format='%d.%m.%Y %H:%M:%S')

    class Meta:
        model = Trace
        fields = ['date', 'was_traced', 'name', 'data', 'date_friendly']
