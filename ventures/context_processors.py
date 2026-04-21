# ventures/context_processors.py
from django.urls import reverse
from .models import Sector, Venture


def ventures_navigation(request):
    """
    Injects nav_sectors into every template context.

    nav_sectors = [
        {
            'name':     'Sector Name',
            'url':      '/ventures/sector-slug/',   ← pre-built, safe
            'ventures': [
                { 'name': 'Venture Name', 'url': '/ventures/sector-slug/venture-slug/' },
                ...
            ]
        },
        ...
    ]

    Templates use  {{ sector.url }}  and  {{ venture.url }}
    — no {% url %} tag needed, so a missing slug never crashes a page.
    """
    nav_sectors = []

    sectors = Sector.objects.filter(is_active=True).order_by('order', 'name')

    for sector in sectors:
        ventures = Venture.objects.filter(
            sector=sector,
            is_active=True
        ).order_by('order', 'name')

        venture_list = []
        for venture in ventures:
            try:
                v_url = reverse(
                    'ventures:venture_detail',
                    kwargs={
                        'sector_slug': sector.slug,
                        'venture_slug': venture.slug,
                    }
                )
            except Exception:
                v_url = '#'

            venture_list.append({
                'name': venture.name,
                'url':  v_url,
            })

        try:
            s_url = reverse(
                'ventures:sector_detail',
                kwargs={'slug': sector.slug}
            )
        except Exception:
            s_url = '#'

        nav_sectors.append({
            'name':     sector.name,
            'url':      s_url,
            'ventures': venture_list,
        })

    return {'nav_sectors': nav_sectors}