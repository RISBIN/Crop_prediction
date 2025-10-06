from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class CropPrediction(models.Model):
    """Model to store crop prediction results."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='crop_predictions'
    )

    # Input Parameters
    nitrogen = models.FloatField(verbose_name=_('Nitrogen (N)'))
    phosphorus = models.FloatField(verbose_name=_('Phosphorus (P)'))
    potassium = models.FloatField(verbose_name=_('Potassium (K)'))
    temperature = models.FloatField(verbose_name=_('Temperature (C)'))
    humidity = models.FloatField(verbose_name=_('Humidity (%)'))
    ph_value = models.FloatField(verbose_name=_('pH Value'))
    rainfall = models.FloatField(verbose_name=_('Rainfall (mm)'))

    # Results
    predicted_crop = models.CharField(max_length=100, verbose_name=_('Predicted Crop'))
    confidence_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Confidence Score')
    )
    top_3_crops = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_('Top 3 Crop Recommendations')
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_('Location')
    )

    class Meta:
        verbose_name = _('Crop Prediction')
        verbose_name_plural = _('Crop Predictions')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.predicted_crop} ({self.created_at.strftime('%Y-%m-%d')})"


class SoilClassification(models.Model):
    """Model to store soil classification results."""

    SOIL_TYPES = [
        ('black', 'Black Soil'),
        ('clay', 'Clay Soil'),
        ('loamy', 'Loamy Soil'),
        ('sandy', 'Sandy Soil'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='soil_classifications'
    )

    # Input
    soil_image = models.ImageField(
        upload_to='soil_images/%Y/%m/%d/',
        verbose_name=_('Soil Image')
    )

    # Results
    soil_type = models.CharField(
        max_length=20,
        choices=SOIL_TYPES,
        verbose_name=_('Soil Type')
    )
    confidence_score = models.FloatField(verbose_name=_('Confidence Score'))
    all_predictions = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('All Predictions')
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_('Location')
    )

    class Meta:
        verbose_name = _('Soil Classification')
        verbose_name_plural = _('Soil Classifications')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_soil_type_display()} ({self.created_at.strftime('%Y-%m-%d')})"


class FertilizerRecommendation(models.Model):
    """Model to store fertilizer recommendations."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fertilizer_recommendations'
    )

    crop_prediction = models.ForeignKey(
        CropPrediction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fertilizer_recommendations'
    )

    # Input Parameters
    crop_name = models.CharField(max_length=100, verbose_name=_('Crop Name'))
    nitrogen = models.FloatField(verbose_name=_('Nitrogen (N)'))
    phosphorus = models.FloatField(verbose_name=_('Phosphorus (P)'))
    potassium = models.FloatField(verbose_name=_('Potassium (K)'))
    soil_type = models.CharField(max_length=20, verbose_name=_('Soil Type'))

    # Recommendations
    recommended_fertilizer = models.CharField(
        max_length=200,
        verbose_name=_('Recommended Fertilizer')
    )
    application_rate = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Application Rate')
    )
    application_timing = models.TextField(
        blank=True,
        verbose_name=_('Application Timing')
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Fertilizer Recommendation')
        verbose_name_plural = _('Fertilizer Recommendations')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.crop_name} ({self.recommended_fertilizer})"


class PredictionHistory(models.Model):
    """Model to track all prediction history for analytics."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='prediction_history'
    )

    prediction_type = models.CharField(
        max_length=50,
        choices=[
            ('crop', 'Crop Prediction'),
            ('soil', 'Soil Classification'),
            ('fertilizer', 'Fertilizer Recommendation'),
        ],
        verbose_name=_('Prediction Type')
    )

    result_summary = models.TextField(verbose_name=_('Result Summary'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Prediction History')
        verbose_name_plural = _('Prediction Histories')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_prediction_type_display()} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
