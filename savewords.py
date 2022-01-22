import os
from os import path
import json
from urllib.parse import quote

import sozlukgetir

SAVEDIR = "sozluk"
os.makedirs(SAVEDIR, exist_ok=True)

print("Fetching word list")
wordList = sozlukgetir.fetch_word_list()

wordlist_save = path.join(SAVEDIR, "tdk-autocomplete.json")
with open(wordlist_save, "w", encoding="utf-8") as fp:
    json.dump(wordList, fp, ensure_ascii=False)
    print(f"Word list saved at '{wordlist_save}'")

os.makedirs(path.join(SAVEDIR, "words"), exist_ok=True)

successList = []
errorList = []
for word in wordList:
    result = sozlukgetir.fetch_details(word)
    if "error" in result:    
        errorList.append((word, result["error"]))
        print(f"No such word: \"{word}\"")
    else:
        successList.append((word,))
        _path = path.join(SAVEDIR, "words", f"{quote(word)}.json")
        with open(_path, "w", encoding="utf-8") as fp:
            json.dump(result, fp, ensure_ascii=False)
        print(f"\"{word}\" saved at '{_path}'")

print("Job done")
print("Total words saved:", len(successList))
print("Total errors:", len(errorList))