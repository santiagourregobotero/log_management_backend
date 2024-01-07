#listings/filters.py
import django_filters
from django.db.models import Q
from .models import SysLog
from datetime import datetime
from django_filters.widgets import RangeWidget

class LogFilter(django_filters.FilterSet):
    class Meta:
      model = SysLog
      fields = ['start_date', 'end_date', 'severity', 'source']
        
    # timestamp = django_filters.DateTimeFromToRangeFilter(label='timestamp')
    start_date = django_filters.Filter(field_name='timestamp', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='timestamp', lookup_expr='lte')
    severity = django_filters.CharFilter(label="severity")
    source = django_filters.CharFilter(label="source", lookup_expr='icontains')
    