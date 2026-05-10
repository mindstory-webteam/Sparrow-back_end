# ventures/views.py
from django.shortcuts import render, get_object_or_404
from .models import Sector, Venture


def sector_list(request):
    """Show all sectors."""
    sectors = Sector.objects.filter(is_active=True)
    return render(request, 'ventures/sector_list.html', {'sectors': sectors})


def sector_detail(request, slug):
    """Show a sector with its ventures."""
    sector   = get_object_or_404(Sector, slug=slug, is_active=True)
    ventures = sector.ventures.filter(is_active=True)
    return render(request, 'ventures/sector_detail.html', {
        'sector':   sector,
        'ventures': ventures,
    })


def venture_detail(request, sector_slug, venture_slug):
    """
    Show venture details page.
    Context passed to template:
        venture          – Venture instance
        venture_about    – VentureAbout instance or None
        areas_of_working – QuerySet[AreaOfWorking]
        features         – QuerySet[Feature]
    """
    venture = get_object_or_404(
        Venture,
        slug=venture_slug,
        sector__slug=sector_slug,
        is_active=True,
    )

    # OneToOne — use hasattr guard so template never raises an exception
    venture_about = getattr(venture, 'about', None)

    return render(request, 'ventures/venture_detail.html', {
        'venture':          venture,
        'venture_about':    venture_about,
        'areas_of_working': venture.areas_of_working.all(),
        'features':         venture.features.all(),
    })