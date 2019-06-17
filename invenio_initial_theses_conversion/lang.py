from langdetect import detect_langs
from sqlalchemy.util import namedtuple

import logging

log = logging.getLogger(__name__)

MatchedLang = namedtuple('MatchedLang', ('lang', 'prob'))


def assert_language(text, expected_language):
    langs = detect_langs(text)
    langs = [
        MatchedLang({
                        'cs': 'cze',
                        'en': 'eng'
                    }.get(x.lang), x.prob) for x in langs
    ]

    if not langs or langs[0].prob < 0.50:
        return expected_language  # unable to decide

    if langs[0].lang != expected_language:
        if langs[0].lang is None:  # unknown language detected
            return expected_language
        if len(text) < 15:  # text too short to say
            return expected_language
        # detected but different
        log.warning('Warning: error: language does not match. Expected %s, has %s, langs %s, value %s',
                    expected_language, langs[0].lang, langs, text)
    if langs:
        # return the detected language
        return langs[0].lang
    return expected_language
