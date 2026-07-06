import keyword
from django.shortcuts import render, get_object_or_404
from django.template import context

import matches
from .models import Match, Country

# Create your views here.

def top(request):
    return render(request, 'history/top.html')

def index(request):
    return render(request, 'history/index.html')


def year_search(request):

    years = (
        Match.objects
        .dates('match_date', 'year', order='DESC')
    )

    selected_year = request.GET.get('year')

    matches = Match.objects.none()

    if selected_year:
        matches = Match.objects.filter(
            match_date__year=selected_year
        ).select_related('country', 'competition')

    context = {
        'years': years,
        'selected_year': selected_year,
        'matches': matches,
    }

    return render(
        request,
        'history/year_search.html',
        context,
    )


def match_detail(request, match_id):

    match = get_object_or_404(
        Match.objects.select_related(
            'country',
            'competition'
        ),
        pk=match_id
    )

    year = request.GET.get('year')
    country_name = request.GET.get('country_name')

    context = {
        'match': match,
        'year': year,
        'country_name':country_name
    }

    return render(
        request, 
        'history/match_detail.html', 
        context)

def country_record(request):

    keyword = request.GET.get(
        'country_name',
        ''
    )

    country = None

    matches = Match.objects.none()

    wins = 0
    draws = 0
    losses = 0

    goals_for = 0
    goals_against = 0

    if keyword:

        country = Country.objects.filter(
            name__icontains=keyword
        ).first()

        if country:

            matches = Match.objects.filter(
                country=country
            ).select_related(
                'competition',
                'country'
            )

            for match in matches:

                goals_for += match.score_japan

                goals_against += match.score_opponent

                if match.score_japan > match.score_opponent:
                    wins += 1

                elif match.score_japan == match.score_opponent:
                    draws += 1

                else:
                    losses += 1

    context = {
        'keyword': keyword,
        'country': country,
        'matches': matches,
        'wins': wins,
        'draws': draws,
        'losses': losses,
        'goals_for': goals_for,
        'goals_against': goals_against,
    }

    return render(
        request,
        'history/country_record.html',
        context,
    )