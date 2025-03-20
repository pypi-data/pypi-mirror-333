from django.urls import path
from database_report import views

urlpatterns = [
    path("database-data/",views.database_report,name="database-data")
]
