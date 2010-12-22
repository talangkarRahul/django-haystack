"""
Placeholder backend which will raise exceptions when called

Used to catch situations where multiple backends are defined without a default
and the user has neglected to specify which backend to use for a query
"""

from haystack.backends import BaseSearchBackend, BaseSearchQuery
from haystack.models import SearchResult

BACKEND_NAME = 'placeholder'


class DummySearchResult(SearchResult):
    pass

class SearchBackend(BaseSearchBackend):
    pass

class SearchQuery(BaseSearchQuery):
    pass