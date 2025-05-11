from serpapi import GoogleSearch
from ..config import api_key_google_trends


class GoogleTrends:
    @staticmethod
    async def get_trends(topic):
        params = {
            "api_key": api_key_google_trends,
            "engine": "google_trends",
            "q": topic,
            "hl": "id",
            "geo": "ID",
            "data_type": "TIMESERIES",
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        return results

    @staticmethod
    async def get_maps(topic):
        is_multiple_topics = len(topic) > 1
        query = ", ".join(topic) if is_multiple_topics else "kopi, teh"
        data_type = "GEO_MAP" if is_multiple_topics else "GEO_MAP_0"

        params = {
            "api_key": api_key_google_trends,
            "engine": "google_trends",
            "q": query,
            "hl": "id",
            "geo": "ID",
            "data_type": data_type,
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        return results
