"""
libs.strings

By default, uses 'en-us.json' file inside the 'strings' top-level folder.
If the language changes, set 'libs.strings.default_locale' and run 'libs.strings.refresh()'

"""

import json

# TODO : switch to flask-babel and read on po edit


class TranslatorException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


default_locale = "en-us"
cached_strings = {}


def change_locale(locale):
    set_default_locale(locale=locale)
    refresh()


def set_default_locale(locale):
    global default_locale
    default_locale = locale


def refresh():
    global cached_strings
    with open(f"strings/{default_locale}.json") as f:
        cached_strings = json.load(f)


def gettext(get_err):
    try:
        return cached_strings.get(get_err)
    except:
        raise TranslatorException(cached_strings.get("err_key_not_found"))


refresh()
