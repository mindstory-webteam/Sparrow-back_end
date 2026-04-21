# ventures/views.py
from django.shortcuts import render, get_object_or_404
from .models import Sector, Venture


def sector_list(request):
    """Show all sectors"""
    sectors = Sector.objects.filter(is_active=True)
    return render(request, 'ventures/sector_list.html', {'sectors': sectors})


def sector_detail(request, slug):
    """Show sector with its ventures"""
    sector = get_object_or_404(Sector, slug=slug, is_active=True)
    ventures = sector.ventures.filter(is_active=True)
    return render(request, 'ventures/sector_detail.html', {
        'sector': sector,
        'ventures': ventures,
    })


def venture_detail(request, sector_slug, venture_slug):
    """
    Show venture details.
    - areas_of_working → left panel list
      each area has .name, .is_operational, .area_image (may be blank)
      clicking an area swaps its image into the right panel
    """
    venture = get_object_or_404(
        Venture,
        slug=venture_slug,
        sector__slug=sector_slug,
        is_active=True
    )
    areas_of_working = venture.areas_of_working.all()  # ordered by ['order', 'name']

    return render(request, 'ventures/venture_detail.html', {
        'venture': venture,
        'areas_of_working': areas_of_working,
    })