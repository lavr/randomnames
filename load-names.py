from __future__ import unicode_literals, print_function
import requests
from requests.adapters import HTTPAdapter

GROUPS = (
    ('fictional-character', 'https://wdq.wmflabs.org/api?q=claim[31:95074]'),
    ('philosophers', 'https://wdq.wmflabs.org/api?q=claim[106:4964182]'),
    ('warriors', 'https://wdq.wmflabs.org/api?q=claim[106:1250916]'),
    ('explorers', 'https://wdq.wmflabs.org/api?q=claim[106:11900058]'),
    ('monarchs', 'https://wdq.wmflabs.org/api?q=claim[39:116]'),
    #('engineers', 'https://wdq.wmflabs.org/api?q=claim[106:Q81096]'),
    #('aerospace-engineers', 'https://wdq.wmflabs.org/api?q=claim[106:Q15895020]'),

)

GROUPS_DICT = dict(GROUPS)

class Loader(object):
    pass


class WikipediaLoader(Loader):

    def __init__(self):
        self.session = requests.Session()
        self.session.mount('https://www.wikidata.org', HTTPAdapter(max_retries=42))
        self.session.mount('https://wdq.wmflabs.org', HTTPAdapter(max_retries=42))

    def get_ids(self, groupname):
        url = GROUPS_DICT[groupname]
        items = self.session.get(url).json()['items']
        return items

    def get_label_by_id(self, item_id):
        if isinstance(item_id, int):
            item_id = "Q{}".format(item_id)
        url = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&languages=en&props=labels&ids={}".format(item_id)
        data = self.session.get(url).json()['entities'][item_id]
        return data.get('labels',{}).get('en', {}).get('value')


class CacheLoader(Loader):
    def __init__(self, filename):
        cache = {}
        for line in open(filename):
            parts = line.strip().split(b':')
            groupname = parts[0]
            id = parts[1]
            label = b":".join(parts[3:])
            cache.setdefault(groupname, []).append(id)
            cache.setdefault('_global', {})[id] = label.decode('utf-8')
        self.cache = cache

    def get_ids(self, groupname):
        return self.cache[groupname]

    def get_label_by_id(self, item_id):
        return self.cache['_global'][str(item_id)]

import re
NON_ASCII = re.compile(r"[^A-Za-z0-9\- ]")
def filter_name(name):
    return not NON_ASCII.search(name)

def is_simple_name(label):
    if not NON_ASCII.search(label) and len(label)>4 and len(label.split(' '))==2:
        return True

def main():
    #loader = WikipediaLoader()
    loader = CacheLoader('names.txt')
    cache = set()
    for title, _ in GROUPS:
        for item in loader.get_ids(groupname=title):
            label = loader.get_label_by_id(item)
            if label and is_simple_name(label):
                for part in label.split(' '):
                    if len(part)>3:
                        if part not in cache:
                            print(part)
                            cache.add(part)
                    #print("{}:{}:{}:{}".format(title, item, b'simple' if is_simple_name(label) else b'complex', label).encode('utf-8'))

if __name__ == "__main__":
    main()

