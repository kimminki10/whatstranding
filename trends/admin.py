from django.contrib import admin
from .models import Trend
# Register your models here.

class TrendAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'search_volume', 'started_at']
    search_fields = ['keyword']

admin.site.register(Trend, TrendAdmin)