from flask import request

LANGUAGES = ["fr", "de"]


def get_locale():
    """try to guess the language from the user accept header the browser transmits"""
    return request.accept_languages.best_match(LANGUAGES)
