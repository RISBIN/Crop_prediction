from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import CropPredictionForm, SoilClassificationForm
from .models import CropPrediction, SoilClassification, PredictionHistory
from .ml_services.crop_predictor import get_crop_predictor
from .ml_services.soil_classifier import get_soil_classifier


@login_required
@require_http_methods(["GET", "POST"])
def crop_prediction_view(request):
    """View for crop prediction."""
    if request.method == 'POST':
        form = CropPredictionForm(request.POST)
        if form.is_valid():
            # Save the prediction with user
            prediction = form.save(commit=False)
            prediction.user = request.user

            # Get ML prediction
            predictor = get_crop_predictor()
            features = {
                'nitrogen': prediction.nitrogen,
                'phosphorus': prediction.phosphorus,
                'potassium': prediction.potassium,
                'temperature': prediction.temperature,
                'humidity': prediction.humidity,
                'ph_value': prediction.ph_value,
                'rainfall': prediction.rainfall,
            }

            result = predictor.predict(features)

            # Update prediction with results
            prediction.predicted_crop = result['predicted_crop']
            prediction.confidence_score = result['confidence_score']
            prediction.top_3_crops = result['top_3_crops']
            prediction.save()

            # Save to history
            PredictionHistory.objects.create(
                user=request.user,
                prediction_type='crop',
                result_summary=f"Predicted crop: {result['predicted_crop']} (Confidence: {result['confidence_score']})"
            )

            messages.success(request, f"Prediction successful! Recommended crop: {result['predicted_crop']}")
            return redirect('predictions:crop_result', pk=prediction.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CropPredictionForm()

    return render(request, 'predictions/crop_prediction.html', {'form': form})


@login_required
def crop_result_view(request, pk):
    """View for displaying crop prediction results."""
    try:
        prediction = CropPrediction.objects.get(pk=pk, user=request.user)
    except CropPrediction.DoesNotExist:
        messages.error(request, "Prediction not found.")
        return redirect('predictions:crop_prediction')

    context = {
        'prediction': prediction,
    }
    return render(request, 'predictions/crop_result.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def soil_classification_view(request):
    """View for soil classification."""
    if request.method == 'POST':
        form = SoilClassificationForm(request.POST, request.FILES)
        if form.is_valid():
            import tempfile
            import os
            from django.core.files.uploadedfile import InMemoryUploadedFile
            from io import BytesIO

            # Get the uploaded file
            uploaded_file = request.FILES['soil_image']

            # Read file content into memory
            file_content = uploaded_file.read()

            # Create a temporary file to pass to the classifier
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(file_content)
                tmp_file_path = tmp_file.name

            try:
                # Get ML classification
                classifier = get_soil_classifier()
                result = classifier.classify(tmp_file_path)

                # Reset the uploaded file for saving
                uploaded_file.seek(0)

                # Now save the classification with all data
                classification = form.save(commit=False)
                classification.user = request.user
                classification.soil_type = result['soil_type']
                classification.confidence_score = result['confidence_score']
                classification.all_predictions = result['all_predictions']
                classification.save()

                # Save to history
                PredictionHistory.objects.create(
                    user=request.user,
                    prediction_type='soil',
                    result_summary=f"Classified as: {classification.get_soil_type_display()} (Confidence: {result['confidence_score']*100:.1f}%)"
                )

                messages.success(request, f"Classification successful! Soil type: {classification.get_soil_type_display()}")
                return redirect('predictions:soil_result', pk=classification.pk)
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SoilClassificationForm()

    return render(request, 'predictions/soil_classification.html', {'form': form})


@login_required
def soil_result_view(request, pk):
    """View for displaying soil classification results."""
    try:
        classification = SoilClassification.objects.get(pk=pk, user=request.user)
    except SoilClassification.DoesNotExist:
        messages.error(request, "Classification not found.")
        return redirect('predictions:soil_classification')

    context = {
        'classification': classification,
    }
    return render(request, 'predictions/soil_result.html', context)


@login_required
def prediction_history_view(request):
    """View for displaying user's prediction history."""
    crop_predictions = CropPrediction.objects.filter(user=request.user)[:10]
    soil_classifications = SoilClassification.objects.filter(user=request.user)[:10]

    context = {
        'crop_predictions': crop_predictions,
        'soil_classifications': soil_classifications,
    }
    return render(request, 'predictions/history.html', context)
