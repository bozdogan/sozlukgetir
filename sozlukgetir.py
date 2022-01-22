from urllib import request
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
LOCATIONS = {
    "autocomplete": "https://sozluk.gov.tr/autocomplete.json",
    "autocompleteSapka": "https://sozluk.gov.tr/assets/js/autocompleteSapka.json",
    "gts": "https://sozluk.gov.tr/gts?ara={query}",
    "yazim": "https://sozluk.gov.tr/yazim?ara={query}"
}

def fetchWordList(url=LOCATIONS["autocomplete"]):
    with request.urlopen(url) as res:
        data = json.loads(res.read())
        return list(map(lambda it: it["madde"], data))

if __name__ == "__main__":
    print("Fetching autocomplete word list")
    wordList = fetchWordList()

    print("WORDS::\n")
    print(wordList)
