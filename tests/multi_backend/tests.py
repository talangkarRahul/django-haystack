from django.test import TestCase
from django.core.management import call_command

from haystack.sites import site
from haystack.query import SearchQuerySet
from haystack import indexes

from models import Post

class PostIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

    def using(self, backend_name):
        r = super(PostIndex, self).using(backend_name)
        r._language = backend_name
        return r

    def get_queryset(self):
        return Post.objects.filter(lang=self._language)

site.register(Post, PostIndex)

class MultiBackendTestCase(TestCase):
    fixtures = ['multi_tests.json']

    def setUp(self):
        call_command("rebuild_index", verbosity=0, interactive=False)

    def test_search(self):
        en_sqs = SearchQuerySet().using("en").auto_query("django")
        es_sqs = SearchQuerySet().using("es").auto_query("django")

        self.assertEqual(len(en_sqs), 1)
        self.assertEqual(len(es_sqs), 1)

        self.assertEqual(en_sqs[0].title, "Django at a glance")
        self.assertEqual(es_sqs[0].title, "Django de un vistazo")
