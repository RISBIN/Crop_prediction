from django.contrib import admin
from .models import CropPrediction, SoilClassification, FertilizerRecommendation, PredictionHistory


@admin.register(CropPrediction)
class CropPredictionAdmin(admin.ModelAdmin):
    """Admin for Crop Predictions."""

    list_display = ('user', 'predicted_crop', 'confidence_score', 'location', 'created_at')
    list_filter = ('predicted_crop', 'created_at', 'location')
    search_fields = ('user__username', 'predicted_crop', 'location')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Info', {
            'fields': ('user', 'location')
        }),
        ('Input Parameters', {
            'fields': ('nitrogen', 'phosphorus', 'potassium', 'temperature',
                      'humidity', 'ph_value', 'rainfall')
        }),
        ('Prediction Results', {
            'fields': ('predicted_crop', 'confidence_score', 'top_3_crops')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SoilClassification)
class SoilClassificationAdmin(admin.ModelAdmin):
    """Admin for Soil Classifications."""

    list_display = ('user', 'soil_type', 'confidence_score', 'location', 'created_at')
    list_filter = ('soil_type', 'created_at')
    search_fields = ('user__username', 'location')
    readonly_fields = ('created_at',)


@admin.register(FertilizerRecommendation)
class FertilizerRecommendationAdmin(admin.ModelAdmin):
    """Admin for Fertilizer Recommendations."""

    list_display = ('user', 'crop_name', 'recommended_fertilizer', 'created_at')
    list_filter = ('crop_name', 'soil_type', 'created_at')
    search_fields = ('user__username', 'crop_name', 'recommended_fertilizer')
    readonly_fields = ('created_at',)


@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    """Admin for Prediction History."""

    list_display = ('user', 'prediction_type', 'result_summary', 'created_at')
    list_filter = ('prediction_type', 'created_at')
    search_fields = ('user__username', 'result_summary')
    readonly_fields = ('created_at',)
