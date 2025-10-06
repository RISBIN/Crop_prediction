from django import forms
from .models import CropPrediction, SoilClassification


class CropPredictionForm(forms.ModelForm):
    """Form for crop prediction input."""

    class Meta:
        model = CropPrediction
        fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature',
                  'humidity', 'ph_value', 'rainfall', 'location']
        widgets = {
            'nitrogen': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nitrogen content (0-140)',
                'step': '0.01',
                'min': '0'
            }),
            'phosphorus': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phosphorus content (5-145)',
                'step': '0.01',
                'min': '0'
            }),
            'potassium': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Potassium content (5-205)',
                'step': '0.01',
                'min': '0'
            }),
            'temperature': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Temperature in C (8-45)',
                'step': '0.01'
            }),
            'humidity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Humidity percentage (14-100)',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'ph_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'pH value (3.5-9.9)',
                'step': '0.01',
                'min': '0',
                'max': '14'
            }),
            'rainfall': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rainfall in mm (20-300)',
                'step': '0.01',
                'min': '0'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your location (optional)'
            }),
        }
        labels = {
            'nitrogen': 'Nitrogen (N)',
            'phosphorus': 'Phosphorus (P)',
            'potassium': 'Potassium (K)',
            'temperature': 'Temperature (C)',
            'humidity': 'Humidity (%)',
            'ph_value': 'pH Value',
            'rainfall': 'Rainfall (mm)',
            'location': 'Location',
        }


class SoilClassificationForm(forms.ModelForm):
    """Form for soil classification upload."""

    class Meta:
        model = SoilClassification
        fields = ['soil_image', 'location']
        widgets = {
            'soil_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location where soil sample was taken (optional)'
            }),
        }
        labels = {
            'soil_image': 'Upload Soil Image',
            'location': 'Location',
        }
