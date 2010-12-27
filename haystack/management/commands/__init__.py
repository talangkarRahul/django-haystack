from optparse import make_option

from django.core.management.base import BaseCommand


class HaystackCommand(BaseCommand):
    base_options = (
        make_option('--backend', action='append', dest='backends', type='string',
            help='The backend to operate on (may be used multiple times; default=all backends)'
        ),
    )
    option_list = BaseCommand.option_list + base_options

    #: dict of SearchBackend name & instance values which the command will use
    search_backends = {}

    site = None

    def process_options(self, options):
        self.verbosity = int(options.get('verbosity', 1))

        if 'site' in options:
            self.site = options.get('site')

        from haystack import get_search_backend, search_backends

        if 'backends' not in options:
            self.search_backends = search_backends
        else:
            self.search_backends = dict((i, get_search_backend(i)) for i in
                                            options['backends'])
