from django.shortcuts import render, redirect
from .models import (
    JourneyMilestone, TeamMember, Brand, JobRole, CareerApplication,
    MapLocation, MapConnection, Testimonial,
    ProgramCategory, ProgramEvent, ProgramImage
)
from django.contrib import messages
from django.http import Http404, JsonResponse
import json


def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')
    locations = MapLocation.objects.filter(is_active=True)
    connections = MapConnection.objects.filter(is_active=True).select_related('from_location', 'to_location')
    locations_data = [{'name': l.name, 'type': l.get_location_type_display(), 'lat': float(l.latitude), 'lng': float(l.longitude), 'address': l.address, 'icon': l.icon, 'category': l.location_type} for l in locations]
    connections_data = [{'from': {'lat': float(c.from_location.latitude), 'lng': float(c.from_location.longitude)}, 'to': {'lat': float(c.to_location.latitude), 'lng': float(c.to_location.longitude)}, 'color': c.color} for c in connections]
    return render(request, 'contact.html', {'page_title': 'Contact Us - Sparrow International', 'active_page': 'contact', 'locations_json': json.dumps(locations_data), 'connections_json': json.dumps(connections_data)})


def Home(request):
    team_members = TeamMember.objects.filter(is_active=True).order_by('order')[:2]
    brands = Brand.objects.filter(is_active=True).order_by('order')
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')
    locations = MapLocation.objects.filter(is_active=True)
    connections = MapConnection.objects.filter(is_active=True).select_related('from_location', 'to_location')
    locations_data = [{'name': l.name, 'type': l.get_location_type_display(), 'lat': float(l.latitude), 'lng': float(l.longitude), 'address': l.address, 'icon': l.icon, 'category': l.location_type} for l in locations]
    connections_data = [{'from': {'lat': float(c.from_location.latitude), 'lng': float(c.from_location.longitude)}, 'to': {'lat': float(c.to_location.latitude), 'lng': float(c.to_location.longitude)}, 'color': c.color} for c in connections]
    return render(request, 'index.html', {'page_title': 'Home - Sparrow International', 'active_page': 'home', 'team_members': team_members, 'brands': brands, 'testimonials': testimonials, 'locations_json': json.dumps(locations_data), 'connections_json': json.dumps(connections_data)})


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
    if request.method == 'POST':
        try:
            full_name = request.POST.get('full_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            job_role = request.POST.get('job_role', '').strip()
            message_text = request.POST.get('message', '').strip()
            if not all([full_name, email, phone, job_role]):
                messages.error(request, 'Please fill in all required fields.')
                return redirect('main:career')
            CareerApplication.objects.create(full_name=full_name, email=email, phone=phone, job_role=job_role, message=message_text)
            messages.success(request, 'Thank you for your application! We will review it and get back to you soon.')
            return redirect('main:career')
        except Exception:
            messages.error(request, 'An error occurred. Please try again later.')
            return redirect('main:career')
    job_roles = JobRole.objects.filter(is_active=True).order_by('order')
    recent_jobs = JobRole.objects.filter(is_active=True, show_in_recent=True).order_by('-posted_date')[:3]
    total_vacancies = sum(job.vacancy_count for job in job_roles)
    return render(request, 'career.html', {'page_title': 'Career - Sparrow International', 'active_page': 'career', 'job_roles': job_roles, 'recent_jobs': recent_jobs, 'total_vacancies': total_vacancies})


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