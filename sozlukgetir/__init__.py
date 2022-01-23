from urllib import request
from urllib.error import URLError, HTTPError
import urllib.parse
import json

LOCATIONS = {
    "autocomplete": "https://sozluk.gov.tr/autocomplete.json",
    "autocompleteSapka": "https://sozluk.gov.tr/assets/js/autocompleteSapka.json",
    "gts": "https://sozluk.gov.tr/gts?ara={madde}",
    "yazim": "https://sozluk.gov.tr/yazim?ara={madde}",
    "ses": "https://sozluk.gov.tr/ses/{seskod}.wav"
}

def fetch_word_list():
    url=LOCATIONS["autocomplete"]
    with request.urlopen(url) as res:
        data = json.loads(res.read())
        return list(map(lambda it: it["madde"], data))

def fetch_details(word):
    word = word.replace("İ", "i").replace("I", "ı").lower()
    url_gts = LOCATIONS["gts"].format(madde=urllib.parse.quote(word, encoding="utf-8"))
    url_yazim = LOCATIONS["yazim"].format(madde=urllib.parse.quote(word, encoding="utf-8"))
    
    def _get(url, ignore_errors=False):
        with request.urlopen(url) as res:
            data = json.loads(res.read())
            if not ignore_errors and "error" in data:  # NOTE: {'error': 'Sonuç bulunamadı'}
                raise Exception("No such result")
            return data
    try:
        result = {}
        result["gts"] = _get(url_gts)
        result["yazim"] = _get(url_yazim, ignore_errors=True)
    except HTTPError as e:
        result = {"error": "HTTPError", "code": e.code}
    except URLError as e:
        result = {"error": "URLError", "reason": e.reason}
    except Exception as e:
        # TODO(bora): User shouldn't see this
        result = {"error": e}
    
    return result
