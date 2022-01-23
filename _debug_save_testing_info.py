import urllib.parse
import urllib.request
import json
import sozlukgetir
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def save_word_test_info(word):
    word = word.replace("İ", "i").replace("I", "ı").lower()
    
    with urllib.request.urlopen(
                sozlukgetir.LOCATIONS["gts"]
                .format(madde=urllib.parse.quote(word))
                ) as response, \
            open(f"word_{word}.sample.gts.json", "w", encoding="utf-8") as fp:
        json.dump(json.loads(response.read()), fp)

    with urllib.request.urlopen(
                sozlukgetir.LOCATIONS["yazim"]
                .format(madde=urllib.parse.quote(word))
            ) as response, \
            open(f"word_{word}.sample.yazim.json", "w", encoding="utf-8") as fp:
        json.dump(json.loads(response.read()), fp)

    with open(f"word_{word}.result.yazim.json", "w", encoding="utf-8") as fp:
        json.dump(sozlukgetir.fetch_details(word), fp)


# save_word_test_info("âdet")
# save_word_test_info("Çiğdem")
# save_word_test_info("Iğdır")
# save_word_test_info("İstanbul")
# save_word_test_info("sözlük")
# save_word_test_info("çıkmak")
# save_word_test_info("Meriç")

print("done")
