from django.conf import settings
from django.test import TestCase
from haystack import site, indexes, __version__ as haystack_version
from haystack.backends.solr_backend import SearchBackend, SearchQuery
from haystack.management.commands.build_solr_schema import Command
from haystack.query import SQ
from core.models import MockModel, AnotherMockModel


class MockModelSearchIndex(indexes.SearchIndex):
    text = indexes.CharField(model_attr='foo', document=True)
    name = indexes.CharField(model_attr='author')
    pub_date = indexes.DateField(model_attr='pub_date')


class AlteredInternalNamesTestCase(TestCase):
    def test_altered_names(self):
        sq = SearchQuery(backend=SearchBackend())
        
        sq.add_filter(SQ(content='hello'))
        sq.add_model(MockModel)
        self.assertEqual(sq.build_query(), u'(hello) AND (my_django_ct:core.mockmodel)')
        
        sq.add_model(AnotherMockModel)
        self.assertEqual(sq.build_query(), u'(hello) AND (my_django_ct:core.anothermockmodel OR my_django_ct:core.mockmodel)')
    
    def test_solr_schema(self):
        site.register(MockModel, MockModelSearchIndex)
        
        command = Command()
        self.assertEqual(command.build_context('default').dicts[0], {
            'DJANGO_ID': 'my_django_id',
            'content_field_name': 'text',
            'backend_settings': {'url': 'http://localhost:9001/solr/test_default', 'include_spelling': True, 'type': 'solr', 'timeout': 10},
            'fields': [
                {
                    'indexed': 'true',
                    'type': 'text',
                    'stored': 'true',
                    'field_name': 'text',
                    'multi_valued': 'false'
                },
                {
                    'indexed': 'true',
                    'type': 'date',
                    'stored': 'true',
                    'field_name': 'pub_date',
                    'multi_valued': 'false'
                },
                {
                    'indexed': 'true',
                    'type': 'text',
                    'stored': 'true',
                    'field_name': 'name',
                    'multi_valued': 'false'
                }
            ],
            'DJANGO_CT': 'my_django_ct',
            'default_operator': 'AND',
            'ID': 'my_id',
            'backend_name': 'default',
            'haystack_version': haystack_version
        })
        
        schema_xml = command.build_template('default')
        self.assertTrue('<uniqueKey>my_id</uniqueKey>' in schema_xml)
        self.assertTrue('<field name="my_id" type="string" indexed="true" stored="true" multiValued="false" required="true"/>' in schema_xml)
        self.assertTrue('<field name="my_django_ct" type="string" indexed="true" stored="true" multiValued="false" />' in schema_xml)
        self.assertTrue('<field name="my_django_id" type="string" indexed="true" stored="true" multiValued="false" />' in schema_xml)
