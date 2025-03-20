from django.contrib import admin
from vto_time.models import TZAbbreviation
from vto_time.models import TimeZone

@admin.register(TZAbbreviation)
class TZAbbrAdmin(admin.ModelAdmin):
    list_display = [
        'offset',
        'abbr',
        'identifier',
    ]
    list_display_links = ['identifier']
    search_fields = [
        'identifier',
        'abbr',
    ]

@admin.register(TimeZone)
class TZAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'std',
        'dst',
    ]
    list_display = [
        'identifier',
        'tz_type',
        'src_file',
        'std',
        'dst',
        'aliases',
    ]
    search_fields = [
        'identifier',
        'std__identifier',
        'dst__identifier',
    ]