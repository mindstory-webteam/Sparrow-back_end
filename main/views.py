from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import (
    JourneyMilestone, TeamMember, Brand, JobRole, CareerApplication,
    MapLocation, MapConnection, Testimonial,
    ProgramCategory, ProgramEvent, ProgramImage, HeroBanner
)
from django.contrib import messages
from django.http import Http404, JsonResponse
import json
import logging

from .emails import send_career_application_email, send_applicant_acknowledgement

logger = logging.getLogger(__name__)


def _script_safe_json(data):
    """json.dumps that is safe to print inside <script> with |safe
    (escapes <, > and & so text like "</script>" in an address cannot break the page)."""
    return (json.dumps(data)
            .replace('<', '\\u003c')
            .replace('>', '\\u003e')
            .replace('&', '\\u0026'))


def get_map_context():
    """locations_json + connections_json used by the Leaflet map on Home and Contact pages."""
    locations = MapLocation.objects.filter(is_active=True)
    connections = MapConnection.objects.filter(
        is_active=True,
        from_location__is_active=True,
        to_location__is_active=True,
    ).select_related('from_location', 'to_location')

    locations_data = [{
        'name': l.name,
        'type': l.get_location_type_display(),
        'lat': float(l.latitude),
        'lng': float(l.longitude),
        'address': l.address,
        'icon': l.icon,
        'category': l.location_type,
    } for l in locations]

    connections_data = [{
        'from': {'lat': float(c.from_location.latitude), 'lng': float(c.from_location.longitude)},
        'to': {'lat': float(c.to_location.latitude), 'lng': float(c.to_location.longitude)},
        'color': c.color,
    } for c in connections]

    return {
        'locations_json': _script_safe_json(locations_data),
        'connections_json': _script_safe_json(connections_data),
    }


def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('main:contact')
    return render(request, 'contact.html', {'page_title': 'Contact Us - Sparrow International', 'active_page': 'contact', **get_map_context()})


def Home(request):
    team_members = TeamMember.objects.filter(is_active=True).order_by('order')[:2]
    brands = Brand.objects.filter(is_active=True).order_by('order')
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')
    hero_banners = HeroBanner.objects.filter(is_active=True).exclude(media='').order_by('order', 'created_at')
    return render(request, 'index.html', {
        'page_title': 'Home - Sparrow International',
        'active_page': 'home',
        'hero_banners': hero_banners,
        'team_members': team_members,
        'brands': brands,
        'testimonials': testimonials,
        **get_map_context(),
    })


def about(request):
    journey_milestones = JourneyMilestone.objects.filter(is_active=True).order_by('order', 'year')
    team_members = TeamMember.objects.filter(is_active=True).order_by('order', 'name')
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')

    # Categories with their events and images — prefetched for performance
    program_categories = ProgramCategory.objects.filter(is_active=True).prefetch_related(
        'events__images'
    ).order_by('order', 'name')

    # Filter to categories that have at least one active event
    active_categories = [c for c in program_categories if c.events.filter(is_active=True).exists()]

    # All active years for the year filter
    program_years = (
        ProgramEvent.objects
        .filter(is_active=True, category__is_active=True)
        .values_list('year', flat=True)
        .distinct()
        .order_by('-year')
    )

    context = {
        'page_title': 'Our Story - Sparrow International',
        'active_page': 'about',
        'journey_milestones': journey_milestones,
        'team_members': team_members,
        'testimonials': testimonials,
        'program_categories': active_categories,
        'program_years': program_years,
    }
    return render(request, 'about.html', context)


def career(request):
    career_url = reverse('main:career') + '#apply'

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        job_role = request.POST.get('job_role', '').strip()
        message_text = request.POST.get('message', '').strip()

        if not all([full_name, email, phone, job_role]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect(career_url)
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return redirect(career_url)

        try:
            application = CareerApplication.objects.create(
                full_name=full_name, email=email, phone=phone,
                job_role=job_role, message=message_text,
            )
        except Exception:
            logger.exception("Career application could not be saved")
            messages.error(request, 'An error occurred. Please try again later.')
            return redirect(career_url)

        # Email the application to HR (Hr@sparrowgroup.in). Never breaks the page if mail fails —
        # the application is already saved in Admin → Career Applications.
        send_career_application_email(application, request)
        send_applicant_acknowledgement(application)

        messages.success(request, 'Thank you for your application! Our HR team will review it and get back to you soon.')
        return redirect(career_url)

    job_roles = JobRole.objects.filter(is_active=True).order_by('order')
    recent_jobs = JobRole.objects.filter(is_active=True, show_in_recent=True).order_by('-posted_date')[:3]
    total_vacancies = sum(job.vacancy_count for job in job_roles)
    return render(request, 'career.html', {
        'page_title': 'Career - Sparrow International',
        'active_page': 'career',
        'job_roles': job_roles,
        'recent_jobs': recent_jobs,
        'total_vacancies': total_vacancies,
    })


def programs_gallery(request):
    """Full Programs Gallery page — Category → Event cards with slider → Lightbox"""
    selected_cat  = request.GET.get('category', '')
    selected_year = request.GET.get('year', '')

    categories_qs = ProgramCategory.objects.filter(is_active=True).prefetch_related(
        'events__images'
    ).order_by('order', 'name')

    all_years = (
        ProgramEvent.objects
        .filter(is_active=True, category__is_active=True)
        .values_list('year', flat=True)
        .distinct()
        .order_by('-year')
    )

    # Build events queryset with optional filters
    events_qs = ProgramEvent.objects.filter(
        is_active=True, category__is_active=True
    ).select_related('category').prefetch_related('images')

    if selected_cat:
        events_qs = events_qs.filter(category__slug=selected_cat)
    if selected_year and selected_year.isdigit():
        events_qs = events_qs.filter(year=int(selected_year))

    events_qs = events_qs.order_by('-year', 'order')

    context = {
        'page_title': 'Programs Gallery - Sparrow International',
        'active_page': 'programs',
        'categories': categories_qs,
        'events': events_qs,
        'all_years': all_years,
        'selected_cat': selected_cat,
        'selected_year': selected_year,
        'total_count': events_qs.count(),
    }
    return render(request, 'programs_gallery.html', context)


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)

def test_404(request):
    raise Http404