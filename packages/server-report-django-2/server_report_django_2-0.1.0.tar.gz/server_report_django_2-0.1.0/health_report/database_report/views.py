
# Create your views here.
from django.shortcuts import render
from database_report.models import DatabaseMetrics
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def database_report(request):
    database_metrics = DatabaseMetrics()
    get_database_metrics = database_metrics.collect_database_metrics()
    
    return Response (get_database_metrics)