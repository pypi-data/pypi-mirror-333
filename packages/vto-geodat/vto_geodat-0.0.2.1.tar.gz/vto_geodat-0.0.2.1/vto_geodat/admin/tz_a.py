from django.contrib import admin

from vto_geodat.models import TZAbbreviation
from vto_geodat.models import TimeZone

# Register your models here.
# admin.site.register(TZAbbreviation)
@admin.register(TZAbbreviation)
class TZAbbrAdmin(admin.ModelAdmin):
    #autocomplete_fields = ['parent']
    list_display = [
        'offset',
        'abbr',
        'identifier',
    ]
    list_display_links = ['identifier']
    # search_fields = ['zone_long', 'parent__zone_long']

# admin.site.register(TimeZone)
@admin.register(TimeZone)
class TZAdmin(admin.ModelAdmin):
    #autocomplete_fields = ['parent']
    list_display = [
        'identifier',
        'tz_type',
        'src_file',
        'std',
        'dst',
        'aliases',
    ]
    # list_display_links = ['zone_long']
    # search_fields = ['zone_long', 'parent__zone_long']