import os
from os import path
import json
from urllib.parse import quote
import threading

import sozlukgetir

SAVEDIR = "sozluk"
os.makedirs(SAVEDIR, exist_ok=True)

wordlist_file = path.join(SAVEDIR, "tdk-autocomplete.json")
if not path.exists(wordlist_file):
    print("Fetching word list")
    wordlist = sozlukgetir.fetch_word_list()
    with open(wordlist_file, "w", encoding="utf-8") as fp:
        json.dump(wordlist, fp, ensure_ascii=False)
        print(f"Word list saved at '{wordlist_file}'")

error_log_file = path.join(SAVEDIR, "savewords-errors.log")

successList = []
errorList = []
os.makedirs(path.join(SAVEDIR, "words"), exist_ok=True)

num_threads = 10
total_items = len(wordlist)
item_per_thread = total_items//num_threads
leftover_items = total_items - item_per_thread*num_threads

print("Total items:", total_items)
print("Item per thread:", item_per_thread)
print("Leftover items:", leftover_items)

def progress_bar(title, done, total):
    os.system("title %s %%%.03f" % (title, done/total))

def log_error(word, error):
    with open(error_log_file, "a", encoding="utf-8") as fp:
        fp.write(f"{word} ::\t{error}\n")

def do_fetch(wordlist):
    for i, word in enumerate(wordlist):
        progress_bar("saving -", i, item_per_thread)
        
        result = sozlukgetir.fetch_details(word)
        if "error" in result:    
            errorList.append((word, result["error"]))
            log_error(word, result)
            print(f"ERROR({word}): {result}")
        else:
            successList.append((word,))
            _path = path.join(SAVEDIR, "words", f"{quote(word)}.json")
            with open(_path, "w", encoding="utf-8") as fp:
                json.dump(result, fp, ensure_ascii=False)
            #print(f"  Saved: {word}\" at '{_path}'")

threads = []
for i in range(num_threads):
    # NOTE(bora): If items don't divide equally, leftover items
    # are added to the first thread.
    range_start = i*item_per_thread + (0 if i == 0 else leftover_items)
    range_end = (i + 1)*item_per_thread + leftover_items
    
    t = threading.Thread(target=do_fetch, args=(wordlist[range_start:range_end],))
    #t.daemon = True
    threads.append(t)

print()
print("Starting threads")

with open(error_log_file, "a", encoding="utf-8") as fp:
    fp.write("-"*40 + "\n")

for i in range(num_threads):
    threads[i].start()

for i in range(num_threads):
    threads[i].join()

print()
print("Job done")
print("Total words saved:", len(successList))
print("Total errors:", len(errorList))

with open(error_log_file, "a", encoding="utf-8") as fp: 
    fp.write("\n\n")
    print("Error log saved: '{error_log_file}'")    
