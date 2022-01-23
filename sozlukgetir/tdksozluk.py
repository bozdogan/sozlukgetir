import json
import pathlib
from unittest.main import main
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Union
from . import wordinfo

def normalize_query(word):
    return word.replace("İ", "i").replace("I", "ı").lower()

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
            ) -> Dict[str, Union[List[str], Any]]:
        """
        Fetches the whole word list. Parses local file if available,
        otherwise tries to fetch from the original source. Returns
        a `dict` with "error" field set on error.
        """

        # TODO(bora): Handle errors properly
        try:
            if localfile and pathlib.Path(localfile).exists():
                with open(localfile, encoding="utf-8") as fp:
                    wordlist = json.load(fp)
            else:
                with urllib.request.urlopen(self.locations["wordlist"]) as res:
                    wordlist = json.loads(res.read())
        except urllib.error.HTTPError as e:
            return {
                "error": "HTTPError",
                "code": e.code}
        except urllib.error.URLError as e:
            return {
                "error": "URLError",
                "reason": e.reason}
        except Exception as e:
            raise e
        
        return list(map(lambda it: it["madde"], wordlist))

    def query_word(self, word: str) -> wordinfo.Word:
        """
        Queries the word and returns the result as a Word object.
        """

        gts_url = self.locations["query"].format(
            query=urllib.parse.quote(normalize_query(word)))
        yazim_url = self.locations["spelling"].format(
            query=urllib.parse.quote(normalize_query(word)))
        
        # TODO(bora): Handle errors properly
        res_query = res_spelling = None
        try:
            with urllib.request.urlopen(gts_url) as res:
                res_query = json.loads(res.read())
            # with urllib.request.urlopen(yazim_url) as res:
            #     res_spelling = json.loads(res.read())
        except urllib.error.HTTPError as e:
            return {
                "error": "HTTPError",
                "code": e.code}
        except urllib.error.URLError as e:
            return {
                "error": "URLError",
                "reason": e.reason}
        except Exception as e:
            raise e
        
        if res_query:
            data = res_query[0]
            return wordinfo.Word(
                word=data["madde"],
                is_proper=bool(int(data["ozel_mi"])),
                is_loanword=bool(int(data["lisan_kodu"])),
                origin=data["lisan"] or None,
                meanings=[
                    wordinfo.Meaning(
                        meaning=it["anlam"],
                        is_verb=bool(int(it["fiil"])),
                        properties=[
                            prop["tam_adi"]
                            for prop in it["ozelliklerListe"]])
                    for it in data["anlamlarListe"]])
        else:
            return {"error": "Sonuç bulunamadı."}
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
    
if __name__ == "__main__":
    
    print(TDKSozluk().query_word("sözlük"))
