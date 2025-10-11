from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def landing_page(request):
    """Landing page with hero section and features."""
    return render(request, 'core/landing.html')


@login_required
def dashboard(request):
    """Main dashboard for logged-in users."""
    return render(request, 'core/dashboard.html')


def about(request):
    """About page with project information."""
    return render(request, 'core/about.html')


def contact(request):
    """Contact page."""
    return render(request, 'core/contact.html')


def error_404(request, exception):
    """Custom 404 error page."""
    return render(request, 'core/404.html', status=404)


def error_500(request):
    """Custom 500 error page."""
    return render(request, 'core/500.html', status=500)
