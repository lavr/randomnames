from __future__ import unicode_literals, print_function
import requests
from requests.adapters import HTTPAdapter


GROUPS = (
    ('fictional-character', 'https://wdq.wmflabs.org/api?q=claim[31:95074]'),
    ('philosophers', 'https://wdq.wmflabs.org/api?q=claim[106:4964182]'),
    ('warriors', 'https://wdq.wmflabs.org/api?q=claim[106:1250916]'),
    ('explorers', 'https://wdq.wmflabs.org/api?q=claim[106:11900058]'),
    ('monarchs', 'https://wdq.wmflabs.org/api?q=claim[39:116]'),
)


session = requests.Session()
session.mount('https://www.wikidata.org', HTTPAdapter(max_retries=42))
session.mount('https://wdq.wmflabs.org', HTTPAdapter(max_retries=42))


def get_label(item_id):
    if isinstance(item_id, int):
        item_id = "Q{}".format(item_id)
    url = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&languages=en&props=labels&ids={}".format(item_id)
    data = session.get(url).json()['entities'][item_id]
    return data.get('labels',{}).get('en', {}).get('value')

import re
NON_ASCII = re.compile(r"[^A-Za-z0-9\- ]")
def filter_name(name):
    return not NON_ASCII.search(name)


def main():
    for title, url in GROUPS:
        items = session.get(url).json()['items']
        for item in items:
            label = get_label(item)
            if label:
                print("{}:{}:{}:{}".format(title, item, 'simple' if filter_name(label) else 'complex', label).encode('utf-8'))

if __name__ == "__main__":
    main()

