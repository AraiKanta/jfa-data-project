from django.contrib import admin

from .models import Competition, Country, Match


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'match_date',
        'competition',
        'country',
        'score_japan',
        'score_opponent',
        'venue',
    )
    list_filter = ('competition', 'match_date')
    search_fields = ('country__name', 'competition__name', 'venue')
    date_hierarchy = 'match_date'
