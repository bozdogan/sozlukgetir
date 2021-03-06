import json
import pathlib
import unittest
import urllib.request

from context import sozlukgetir, _abspath, _url
from sozlukgetir import tdksozluk, wordinfo


class TestTDKSozluk(unittest.TestCase):
    def setUp(self) -> None:
        self.offline_test_dir = "./data/core"
        self.local_raw_wordlist = _abspath(f"{self.offline_test_dir}/autocomplete.sample.json")
        self.parsed_wordlist_url = _url(f"{self.offline_test_dir}/wordlist.result.json")
        self.sozluk = sozlukgetir.tdksozluk.TDKSozluk()

        self.sozluk.locations["wordlist"] = _url(self.local_raw_wordlist)
        self.sozluk.locations["diacritics"] = ""
        self.sozluk.locations["query"] = _url(f"{self.offline_test_dir}/word_") + "{query}.sample.gts.json"
        self.sozluk.locations["spelling"] = _url(f"{self.offline_test_dir}/word_") + "{query}.sample.yazim.json"
        self.sozluk.locations["audio"] = ""
    
    def test_get_wordlist(self):
        wordlist = self.sozluk.get_wordlist()
        with urllib.request.urlopen(self.parsed_wordlist_url) as response:
            expected_word_list = json.load(response)
        self.assertEqual(wordlist, expected_word_list)
    
    def test_get_wordlist_local(self):
        _wordlist_url = self.sozluk.locations["wordlist"]
        self.sozluk.locations["wordlist"] = ""

        print(self.local_raw_wordlist)
        wordlist = self.sozluk.get_wordlist(self.local_raw_wordlist)
        with urllib.request.urlopen(self.parsed_wordlist_url) as response:
            expected_word_list = json.load(response)

        self.sozluk.locations["wordlist"] = _wordlist_url
        self.assertEqual(wordlist, expected_word_list)

    
    def test_querying_word(self):
        word = self.sozluk.query_word("sözlük")
        word_expected = wordinfo.Word(
            word='sözlük',
            is_proper=False,
            is_loanword=False,
            origin=None,
            meanings=[
                wordinfo.Meaning(
                    meaning='Bir dilin bütün veya belli bir çağda kullanılmış kelime ve deyimlerini alfabe sırasına göre alarak tanımlarını yapan, açıklayan, başka dillerdeki karşılıklarını veren eser, lügat',
                    is_verb=False,
                    properties=['isim'])])
        self.assertEqual(word, word_expected)
    
    def _combine_word_info(self, word):
        lowercase_word = tdksozluk.normalize_query(word)
        details = sozlukgetir.fetch_details(word)

        with urllib.request.urlopen(self.sozluk.locations["query"].format(query=lowercase_word)) as response:
            gts_data = json.load(response)
        
        with urllib.request.urlopen(self.sozluk.locations["spelling"].format(query=lowercase_word)) as response:
            yazim_data = json.load(response)
        
        return details, gts_data, yazim_data


if __name__ == "__main__":
    unittest.main()
