from __future__ import unicode_literals, print_function
import requests

GROUPS = (
    ('fictional-character', 'https://wdq.wmflabs.org/api?q=claim[31:95074]'),
    ('philosophers', 'https://wdq.wmflabs.org/api?q=claim[106:4964182]'),
    ('warriors', 'https://wdq.wmflabs.org/api?q=claim[106:1250916]'),
    ('explorers', 'https://wdq.wmflabs.org/api?q=claim[106:11900058]'),
    ('monarchs', 'https://wdq.wmflabs.org/api?q=claim[39:116]'),
)


def get_label(item_id):
    if isinstance(item_id, int):
        item_id = "Q{}".format(item_id)
    url = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids={}".format(item_id)
    data = requests.get(url).json()['entities'][item_id]
    return data['labels'].get('en', {}).get('value')


def main():
    for title, url in GROUPS:
        items = requests.get(url).json()['items']
        for item in items:
            label = get_label(item)
            if label:
                print("{}:{}:{}".format(title, item, label.lower()))

if __name__ == "__main__":
    main()
