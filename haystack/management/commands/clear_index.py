from optparse import make_option
import sys
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Clears out the search index completely."
    base_options = (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='If provided, no prompts will be issued to the user and the data will be wiped out.'
        ),
    )

    option_list = BaseCommand.option_list + base_options + (
        make_option('--backend', action='append', dest='backends', type='string',
            help='The backend to operate on (may be used multiple times; default=all backends)'
        ),
    )

    def handle(self, **options):
        """Clears out the search index completely."""
        # Cause the default site to load.
        from haystack import site
        self.verbosity = int(options.get('verbosity', 1))
        
        if options.get('interactive', True):
            print
            print "WARNING: This will irreparably remove EVERYTHING from your search index."
            print "Your choices after this are to restore from backups or rebuild via the `rebuild_index` command."
            
            yes_or_no = raw_input("Are you sure you wish to continue? [y/N] ")
            print
            
            if not yes_or_no.lower().startswith('y'):
                print "No action taken."
                sys.exit()
        
        if self.verbosity >= 1:
            print "Removing all documents from your index because you said so."

        from haystack import get_search_backend, search_backends

        if not options['backends']:
            search_backends = search_backends.values()
        else:
            search_backends = map(get_search_backend, options['backends'])

        for sb in search_backends:
            sb.clear()

        if self.verbosity >= 1:
            print "All documents removed."
