import json
import pathlib
import urllib.parse
import urllib.request

from typing import List, Union

class TDKSozluk:
    def __init__(self):
        self.locations = {
            "wordlist": "https://sozluk.gov.tr/autocomplete.json",
            "diacritics": "https://sozluk.gov.tr/assets/js/autocompleteSapka.json",
            "query": "https://sozluk.gov.tr/gts?ara={query}",
            "spelling": "https://sozluk.gov.tr/yazim?ara={query}",
            "audio": "https://sozluk.gov.tr/ses/{audio}.wav"
        }

    def get_wordlist(
            self,
            localfile: Union[str, pathlib.Path]=None
            ) -> List[str]:
        """
        Fetches the whole word list. Parses local file if available,
        otherwise tries to fetch from the original source. Returns
        nothing if everything fails.
        """

        wordlist = None
        try:
            if localfile and pathlib.Path(localfile).exists():
                with open(localfile, encoding="utf-8") as fp:
                    wordlist = json.load(fp)
            else:
                with urllib.request.urlopen(self.locations["wordlist"]) as res:
                    wordlist = json.loads(res.read())
        except Exception as e:
            raise e
        
        if wordlist:
            return list(map(lambda it: it["madde"], wordlist))


