from django.shortcuts import render, redirect
from .models import JourneyMilestone, TeamMember, Brand, JobRole, CareerApplication, MapLocation, MapConnection, Testimonial
from django.contrib import messages
from django.http import Http404
import json


def contact(request):
    """Contact page view with form handling and dynamic map"""

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comments = request.POST.get('comments')

        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')

    locations = MapLocation.objects.filter(is_active=True)
    connections = MapConnection.objects.filter(is_active=True).select_related(
        'from_location', 'to_location'
    )

    locations_data = []
    for loc in locations:
        locations_data.append({
            'name': loc.name,
            'type': loc.get_location_type_display(),
            'lat': float(loc.latitude),
            'lng': float(loc.longitude),
            'address': loc.address,
            'icon': loc.icon,
            'category': loc.location_type
        })

    connections_data = []
    for conn in connections:
        connections_data.append({
            'from': {
                'lat': float(conn.from_location.latitude),
                'lng': float(conn.from_location.longitude)
            },
            'to': {
                'lat': float(conn.to_location.latitude),
                'lng': float(conn.to_location.longitude)
            },
            'color': conn.color
        })

    context = {
        'page_title': 'Contact Us - Sparrow International',
        'active_page': 'contact',
        'locations_json': json.dumps(locations_data),
        'connections_json': json.dumps(connections_data),
    }

    return render(request, 'contact.html', context)


def Home(request):
    """Home page view with dynamic map and testimonials"""

    team_members = TeamMember.objects.filter(
        is_active=True
    ).order_by('order')[:2]

    brands = Brand.objects.filter(
        is_active=True
    ).order_by('order')

    # ✅ Fetch active testimonials
    testimonials = Testimonial.objects.filter(
        is_active=True
    ).order_by('order')

    locations = MapLocation.objects.filter(is_active=True)
    connections = MapConnection.objects.filter(is_active=True).select_related(
        'from_location', 'to_location'
    )

    locations_data = []
    for loc in locations:
        locations_data.append({
            'name': loc.name,
            'type': loc.get_location_type_display(),
            'lat': float(loc.latitude),
            'lng': float(loc.longitude),
            'address': loc.address,
            'icon': loc.icon,
            'category': loc.location_type
        })

    connections_data = []
    for conn in connections:
        connections_data.append({
            'from': {
                'lat': float(conn.from_location.latitude),
                'lng': float(conn.from_location.longitude)
            },
            'to': {
                'lat': float(conn.to_location.latitude),
                'lng': float(conn.to_location.longitude)
            },
            'color': conn.color
        })

    context = {
        'page_title': 'Home - Sparrow International',
        'active_page': 'home',
        'team_members': team_members,
        'brands': brands,
        'testimonials': testimonials,          # ✅ added
        'locations_json': json.dumps(locations_data),
        'connections_json': json.dumps(connections_data),
    }

    return render(request, 'index.html', context)


def about(request):
    """About page view with dynamic content"""

    journey_milestones = JourneyMilestone.objects.filter(
        is_active=True
    ).order_by('order', 'year')

    team_members = TeamMember.objects.filter(
        is_active=True
    ).order_by('order', 'name')

    # ✅ Fetch active testimonials for about page too
    testimonials = Testimonial.objects.filter(
        is_active=True
    ).order_by('order')

    context = {
        'page_title': 'Our Story - Sparrow International',
        'active_page': 'about',
        'journey_milestones': journey_milestones,
        'team_members': team_members,
        'testimonials': testimonials,          # ✅ added
    }

    return render(request, 'about.html', context)


def career(request):
    """Career page view with application form handling"""

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

            CareerApplication.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                job_role=job_role,
                message=message_text
            )

            messages.success(
                request,
                'Thank you for your application! We will review it and get back to you soon.'
            )
            return redirect('main:career')

        except Exception as e:
            messages.error(request, 'An error occurred. Please try again later.')
            return redirect('main:career')

    job_roles = JobRole.objects.filter(is_active=True).order_by('order')
    recent_jobs = JobRole.objects.filter(
        is_active=True,
        show_in_recent=True
    ).order_by('-posted_date')[:3]
    total_vacancies = sum(job.vacancy_count for job in job_roles)

    context = {
        'page_title': 'Career - Sparrow International',
        'active_page': 'career',
        'job_roles': job_roles,
        'recent_jobs': recent_jobs,
        'total_vacancies': total_vacancies,
    }

    return render(request, 'career.html', context)


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def test_404(request):
    raise Http404