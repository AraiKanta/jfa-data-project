from django.shortcuts import render
from .models import Match

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
