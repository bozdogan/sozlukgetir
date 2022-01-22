import os
from os import path
import json
from urllib.parse import quote
import threading

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

def do_fetch(wordList):
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
            print(f"\"  Saved: {word}\" at '{_path}'")

num_threads = 10
total_items = len(wordList)
item_per_thread = total_items//num_threads
leftover_items = total_items - item_per_thread*num_threads

print("Total items:", total_items)
print("Item per thread:", item_per_thread)
print("Leftover items:", leftover_items)

threads = []
for i in range(num_threads):
    # NOTE(bora): If items don't divide equally, leftover items
    # are added to the first thread.
    range_start = i*item_per_thread + (0 if i == 0 else leftover_items)
    range_end = (i + 1)*item_per_thread + leftover_items
    
    t = threading.Thread(target=do_fetch, args=(wordList[range_start:range_end],))
    #t.daemon = True
    threads.append(t)

print()
print("Starting threads")
for i in range(num_threads):
    threads[i].start()

for i in range(num_threads):
    threads[i].join()

print()
print("Job done")
print("Total words saved:", len(successList))
print("Total errors:", len(errorList))
