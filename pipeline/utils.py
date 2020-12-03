#!/usr/bin/env python3
"""
    Author: Ondrej Mekota o(at)mkta.eu
"""

import os
import json
from typing import List, Dict, Iterator

from lxml import etree

FILE_PATH = os.path.dirname(__file__)

def get_config():
    """ Load json config file and return it in dict. """
    path = os.path.join('config', 'config.json')
    with open(path) as f:
        return json.load(f)


def alignment_to_xml(links:list, path_src, path_tgt):
    """ Converts aligned documents to XML

    Args:
        links: a list of (tuple('type'), list('from'), list('to))
                e.g. ((1,2), [23], [22, 23])

    Returns:
        str of XML

    """
    src_name = os.path.basename(path_src)
    tgt_name = os.path.basename(path_tgt)
    doc = etree.Element('linkGrp', attrib={'toDoc': src_name, 'fromDoc': tgt_name})

    for (t0, t1), from_, to_ in links:
        attr = {
                'type': f'{t0}-{t1}',
                'xtargets': f'{" ".join(map(str, from_))};{" ".join(map(str, to_))}',
                'status': 'null'  # TODO what should be here
        }
        link = etree.SubElement(doc, 'link', attrib=attr)
    return etree.tostring(doc, pretty_print=True, method='xml', encoding='unicode')

def output_to_xml(sents_iter: Iterator[List[Dict]], id_: str, lang:str):
    """ This takes output of a tagger (udpipe, treetagger, ...)
    and converts it to TEI XML.

    Args:
        sents_iter: output of a tagger, iterator over sentences
        id_: id of the document
        lang: 3 letter lang code

    Returns:
        string of TEI XML (as defined by intercorp)

    """

    with open(os.path.join(FILE_PATH, '..', 'config', 'output-schema.json')) as f:
        elems = json.load(f)

    xmlns = 'http://www.korpus.cz/imfSchema'
    xsi = 'http://www.w3.org/2001/XMLSchema-instance'
    schemaLocation = 'http://utils.korpus.cz/xml/schema/cnkImfSchema.xsd'
    doc = etree.Element('doc',
                        attrib={f'{{{xsi}}}schemaLocation': schemaLocation, 'id': id_},
                        nsmap={'xsi':xsi, None:xmlns}
                       )
    attr_text = elems['text']
    attr_text.update({'id': id_, 'lang': lang})
    text_element = etree.SubElement(doc, 'text', attrib=attr_text)

    attr_p = elems['p']
    p_element = etree.SubElement(text_element, 'p', attrib=attr_p)

    for i, s in enumerate(sents_iter):
        attr_s = elems['s']
        attr_s.update({'id': str(i)})
        s_element = etree.SubElement(p_element, 's', attrib=attr_s)
        for w in s:
            # w always has w['word']
            # w always has w['lemma']
            # w can have 'word_trans' and 'lemma_trans'
            # w can have more keys

            word = w['word']
            lemma = w['lemma']
            w.pop('word')
            w.pop('lemma')

            attr_w = elems['w']
            if 'word_trans' in w:
                attr_w.update({'word_trans': w['word_trans'], 'lemma_trans': w['lemma_trans']})

            w.pop('word_trans', None) # try to pop transliterated
            w.pop('lemma_trans', None)

            attr_w.update({'lemma': lemma, 'tag': ' '.join(w.values())})
            w_element = etree.SubElement(s_element, 'w', attrib=attr_w)
            w_element.text = word

    return etree.tostring(doc, pretty_print=True, method='xml', encoding='unicode')


def save_output(text:str, path_original:str, out_dir:str, ext:str):
    """ Saves `text` to `out_dir`/{filename of `path_original`} """
    file_name = os.path.basename(path_original)
    output_path = os.path.join(out_dir, f'{file_name}{ext}')
    # TODO gzip option?
    with open(output_path, 'w') as f:
        f.write(text)

def parse_input_files(files:list, config):
    """ Gets list of files and returns dict with book keys, and lang, version list of values

    Args:
        files: list of file paths [../hobbit_ENG_a.txt, ...]

    Returns:
        tuple of 
        {'hobbit': [('eng', 'a', '../hobbit_ENG_a.txt'), ('pol', 'a', ...)...], ...}
        and 
        {'eng': [('hobbit', 'a', '../hobbit_END_a.txt'), ('prince', 'a', ...)...], ...}


    """
    basenames = map(os.path.basename, files)
    book_files = {}
    for name, file in zip(basenames, files):
        noext = name.split('.')[0]
        split = noext.split('_')

        book_name = split[0]
        book_name_lower = book_name.lower()

        lang = split[1].lower()
        if lang not in config:
            print('WARNING: language code "{lang}" is not in the config')
            continue

        version = None
        if len(split) == 3:
            version = split[2]

        if book_name_lower not in book_files:
            book_files[book_name_lower] = []
        book_files[book_name_lower].append((lang, version, file))

    lang_files = book_files_to_lang_files(book_files)

    return book_files, lang_files

def book_files_to_lang_files(book_files:dict):
    """ Converts output of first item of the output of `parse_input_files` which is a dict with book keys
    to a dict with lang keys.

    Args:
        book_files: dict with structure same as the first item in the output of `parse_input_files`

    Returns:
        {'eng': [('hobbit', 'a', '../hobbit_END_a.txt'), ('prince', 'a', ...)...], ...}

    """
    lang_files = {}
    for book, files in book_files.items():
        for lang, version, file in files:
            if lang not in lang_files:
                lang_files[lang] = []
            lang_files[lang].append((book, version, file))
    return lang_files


def get_polyglot_lang_code(config:dict, lang:str):
    if lang not in config:
        raise ValueError(f'ERROR: language code {lang} is not in the config')

    if 'polyglot_code' not in config[lang]:
        raise ValueError(f'ERROR: language {lang} is not configure to be transliterated')
    polyglot_code = config[lang]['polyglot_code']
    return polyglot_code
