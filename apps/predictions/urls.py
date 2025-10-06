from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    path('crop/', views.crop_prediction_view, name='crop_prediction'),
    path('crop/result/<int:pk>/', views.crop_result_view, name='crop_result'),
    path('soil/', views.soil_classification_view, name='soil_classification'),
    path('soil/result/<int:pk>/', views.soil_result_view, name='soil_result'),
    path('history/', views.prediction_history_view, name='history'),
]
