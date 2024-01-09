from rest_framework import generics, pagination
from django.shortcuts import render
from .models import SysLog
from .serializers import LogSerializer
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import status
from django.db.models import Q
from rest_framework.views import APIView
import logging
import csv
from .filters import LogFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse

logger = logging.getLogger(__name__)

class BasicSizePagination(pagination.PageNumberPagination):
    page_size_query_param  = 'size'
    
    
class LogListCreateView(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = SysLog.objects.all()
    serializer_class = LogSerializer
    pagination_class = BasicSizePagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('source', 'id', 'severity', 'message', )
    filterset_class = LogFilter
    
    def get(self, request):
        query_set = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(query_set)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)


def download_logs(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="your_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'timestamp', 'message', 'severity', 'source'])  # Add column headers

    # Query your data from the database and write to CSV
    queryset = SysLog.objects.all()
    for obj in queryset:
        writer.writerow([obj.id, obj.timestamp, obj.message, obj.severity, obj.source])  # Add other fields as needed

    return response


class LogDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = SysLog.objects.all()
    serializer_class = LogSerializer

    
class LogAnalyticsView(APIView):
    authentication_classes = []
    permission_classes = []
    queryset = SysLog.objects.all()
    serializer_class = LogSerializer
    filter_backends = (DjangoFilterBackend)
    filterset_class = LogFilter
    
    def get(self, request, *args, **kwargs):
        query_set = self.filter_queryset(self.get_queryset())
        aggregated_data = query_set.values('severity', 'source').annotate(count=Count('id')).order_by('severity', 'source')

        return Response(aggregated_data, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            severity = request.GET.get('severity')
            source = request.GET.get('source')
            constraint = request.GET.get('constraint')
            
            filter_conditions = {}
            if start_date:
                filter_conditions['timestamp__gte'] = start_date
            if end_date:
                filter_conditions['timestamp__lte'] = end_date
            if severity:
                filter_conditions['severity'] = severity
            if source:
                filter_conditions['source'] = source
            
            aggregated_data = SysLog.objects.filter(**filter_conditions).values(constraint) \
                .annotate(count=Count('id')).order_by(constraint)

            return Response(aggregated_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error in LogAnalyticsView for aggregation: {e}")
            return Response({'error': 'An internal server error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
