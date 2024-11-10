from celery import shared_task
from .models import Trend
from datetime import datetime
import feedparser

@shared_task
def fetch_google_trends():
    feed = feedparser.parse('https://trends.google.com/trending/rss?geo=KR')
    
    for entry in feed.entries:
        title = entry.title
        search_volume = entry.get('ht_approx_traffic', '0').replace('+', '').replace(',', '')

        try:
            started_at = datetime.strptime(entry.get('published'), '%a, %d %b %Y %H:%M:%S %z')
        except ValueError:
            started_at = None

        try:
            search_volume = int(search_volume)
        except ValueError:
            search_volume = 0

        try:
            search_volume = int(search_volume)
        except ValueError:
            search_volume = 0

        # Save to Trend model if started_at is valid
        if started_at:
            Trend.objects.create(
                keyword=title,
                search_volume=search_volume,
                started_at=started_at
            )