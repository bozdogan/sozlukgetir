import json
import unittest
import urllib.request

from context import sozlukgetir, _url


parsed_word_list_url = _url("./data/core/wordlist.result.json")
dictionary_entry_template = _url("./data/core/word_") + "{madde}.sample.gts.json"
spelling_entry_template = _url("./data/core/word_") + "{madde}.sample.yazim.json"

sozlukgetir.LOCATIONS["autocomplete"] = _url("./data/core/autocomplete.sample.json")  #"https://sozluk.gov.tr/assets/js/autocomplete.json"
sozlukgetir.LOCATIONS["autocompleteSapka"] = ""  #"https://sozluk.gov.tr/assets/js/autocompleteSapka.json"
sozlukgetir.LOCATIONS["gts"] = dictionary_entry_template  #"https://sozluk.gov.tr/gts?ara={madde}"
sozlukgetir.LOCATIONS["yazim"] = spelling_entry_template  #"https://sozluk.gov.tr/yazim?ara={madde}"
sozlukgetir.LOCATIONS["ses"] = ""  #"https://sozluk.gov.tr/ses/{seskod}.wav"


class TestBasic(unittest.TestCase):
    def test_fetching_and_parsing_word_list(self):
        word_list = sozlukgetir.fetch_word_list()
        with urllib.request.urlopen(parsed_word_list_url) as response:
            expected_word_list = json.load(response)
        
        self.assertEqual(word_list, expected_word_list)

    def test_word_details_1(self):
        word_details, gts_data, yazim_data = TestBasic._combine_word_info("sözlük")
        expected_word_details = {"gts": gts_data, "yazim": yazim_data}
        self.assertEqual(word_details, expected_word_details)

    def test_word_details_2(self):
        word_details, gts_data, yazim_data = TestBasic._combine_word_info("çıkmak")
        expected_word_details = {"gts": gts_data, "yazim": yazim_data}
        self.assertEqual(word_details, expected_word_details)
    
    def test_word_details_with_multiple_entries(self):
        word_details, gts_data, yazim_data = TestBasic._combine_word_info("adet")
        expected_word_details = {"gts": gts_data, "yazim": yazim_data}
        self.assertEqual(word_details, expected_word_details)
    
    def test_word_details_capital_letters_1(self):
        word_details, gts_data, yazim_data = TestBasic._combine_word_info("Âdet")
        expected_word_details = {"gts": gts_data, "yazim": yazim_data}
        self.assertEqual(word_details, expected_word_details)
    
    def test_word_details_capital_letters_2(self):
        word_details, gts_data, yazim_data = TestBasic._combine_word_info("Çiğdem")
        expected_word_details = {"gts": gts_data, "yazim": yazim_data}
        self.assertEqual(word_details, expected_word_details)
    
    def test_word_details_capital_letters_3(self):
        word_details, gts_data, yazim_data = TestBasic._combine_word_info("Iğdır")
        expected_word_details = {"gts": gts_data, "yazim": yazim_data}
        self.assertEqual(word_details, expected_word_details)
    
    def test_word_details_capital_letters_4(self):
        word_details, gts_data, yazim_data = TestBasic._combine_word_info("İstanbul")
        expected_word_details = {"gts": gts_data, "yazim": yazim_data}
        self.assertEqual(word_details, expected_word_details)

    @staticmethod
    def _combine_word_info(word):
        lowercase_word = word.replace("İ", "i").replace("I", "ı").lower()
        details = sozlukgetir.fetch_details(word)
        with urllib.request.urlopen(dictionary_entry_template.format(madde=lowercase_word)) as response:
            gts_data = json.load(response)
        with urllib.request.urlopen(spelling_entry_template.format(madde=lowercase_word)) as response:
            yazim_data = json.load(response)
        return details, gts_data, yazim_data


if __name__ == "__main__":
    unittest.main()
