# These tests use multiple Whoosh instances to simulate
# a multi-lingual site with separate English and Spanish
# indices

import os
from settings import *

INSTALLED_APPS += [
    'multi_backend',
]

HAYSTACK_INCLUDE_SPELLING = True

HAYSTACK_SEARCH_ENGINES = {
    'en': {
        'type': 'whoosh',
        'path': os.path.join('tmp', 'test_whoosh_en')
    },
    'es': {
        'type': 'whoosh',
        'path': os.path.join('tmp', 'test_whoosh_es')
    }
}
    
