import os

_input_dir = 'corpuses'

_corpuses = [
    {
        'filename': 'english_ex.txt',
        'lang': 'en',
    },
    {
        'filename': 'finnish_short.txt',
        'lang': 'fl',
    },
    {
        'filename': 'english1.txt',
        'lang': 'en',
    },
    {
        'filename': 'english2.txt',
        'lang': 'en',
    },
    {
        'filename': 'english3.txt',
        'lang': 'en',
    },
    {
        'filename': 'english4.txt',
        'lang': 'en',
        'charset': 'ISO-8859-2',
    },
    {
        'filename': 'finnish1.txt',
        'lang': 'fl',
        'charset': 'iso-8859-9',
    },
    {
        'filename': 'finnish2.txt',
        'lang': 'fl',
        'charset': 'iso-8859-9',
    },
    {
        'filename': 'german1.txt',
        'lang': 'de',
        'charset': 'iso-8859-1',
    },
    {
        'filename': 'german2.txt',
        'lang': 'de',
        'charset': 'iso-8859-1',
    },
    {
        'filename': 'german3.txt',
        'lang': 'de',
        'charset': 'iso-8859-1',
    },
    {
        'filename': 'german4.txt',
        'lang': 'de',
        'charset': 'iso-8859-1',
    },
    {
        'filename': 'italian1.txt',
        'lang': 'it',
    },
    {
        'filename': 'italian2.txt',
        'lang': 'it',
    },
    {
        'filename': 'polish1.txt',
        'lang': 'pl',
        'charset': 'iso-8859-2',
    },
    {
        'filename': 'polish2.txt',
        'lang': 'pl',
        'charset': 'iso-8859-2',
    },
    {
        'filename': 'polish3.txt',
        'lang': 'pl',
        'charset': 'iso-8859-2',
    },
    {
        'filename': 'spanish1.txt',
        'lang': 'es',
        'charset': 'iso-8859-9',
    },
    {
        'filename': 'spanish2.txt',
        'lang': 'es',
        'charset': 'iso-8859-9',
    },
]


def get_corpuses():
    result = _corpuses
    for c in result:
        c['filename'] = os.path.join(_input_dir, c['filename'])
    return result


def languages_set():
    langs = set()
    for f in _corpuses:
        langs.add(f['lang'])
    return list(langs)
