from rest_framework import serializers
from .models import Trace


class TraceSerializer(serializers.ModelSerializer):
    date_friendly = serializers.DateTimeField(source='date', format='%d.%m.%Y %H:%M:%S')
    data = serializers.SerializerMethodField()

    class Meta:
        model = Trace
        fields = ['date', 'was_traced', 'name', 'data', 'date_friendly']

    def get_data(self, obj):
        return [result for result in obj.data.split(" ; ")]
