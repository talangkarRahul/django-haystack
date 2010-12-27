from optparse import make_option
import os
import sys

from django.conf import settings
from django.template import loader, Context

from haystack.constants import ID, DJANGO_CT, DJANGO_ID, DEFAULT_OPERATOR
from haystack.management.commands import HaystackCommand

class Command(HaystackCommand):
    help = "Generates a Solr schema that reflects the indexes."
    base_options = (
        make_option("-f", "--filename", action="store", type="string", dest="filename",
                    help='If provided, directs output to a file instead of stdout.'
                    ' %%(backend)s will be expanded if present; otherwise the'
                    ' backend name will be placed before the file extension'),
    )
    option_list = HaystackCommand.option_list + base_options

    def handle(self, **options):
        """Generates a Solr schema that reflects the indexes."""

        self.process_options(options)

        base_filename = options.get('filename')

        if base_filename and '%(backend)s' not in base_filename:
            # If the base_filename doesn't already contain a template value
            # we'll insert it before the extension:
            base_filename = "%s.%%(backend)s%s" % os.path.splitext(base_filename)

        for name in self.search_backends:
            schema_xml = self.build_template(name)

            if base_filename:
                self.write_file(base_filename % {"backend": name}, schema_xml)
            else:
                self.print_stdout(schema_xml, backend_name=name)

    def build_context(self, name):
        # Cause the default site to load.
        from haystack import site, get_search_backend, __version__ as haystack_version

        content_field_name, fields = get_search_backend(name).build_schema(site.all_searchfields())

        return Context({
            'backend_name': name,
            'backend_settings': settings.HAYSTACK_SEARCH_ENGINES[name],
            'content_field_name': content_field_name,
            'fields': fields,
            'default_operator': DEFAULT_OPERATOR,
            'ID': ID,
            'DJANGO_CT': DJANGO_CT,
            'DJANGO_ID': DJANGO_ID,
            'haystack_version': haystack_version
        })

    def build_template(self, name):
        t = loader.get_template('search_configuration/solr.xml')
        c = self.build_context(name)
        return t.render(c)

    def print_stdout(self, schema_xml, backend_name=None):
        sys.stderr.write("\n")
        sys.stderr.write("\n")
        sys.stderr.write("\n")
        sys.stderr.write("Save the following output to 'schema.xml' and place it in your Solr configuration directory.\n")
        sys.stderr.write("--------------------------------------------------------------------------------------------\n")

        if backend_name:
            sys.stderr.write("Backend: %s\n" % backend_name)
            sys.stderr.write("--------------------------------------------------------------------------------------------\n")

        sys.stderr.write("\n")
        print schema_xml

    def write_file(self, filename, schema_xml):
        schema_file = open(filename, 'w')
        schema_file.write(schema_xml)
        schema_file.close()
