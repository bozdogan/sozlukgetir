import os
from os import path
import sys
import json
import threading
import time
import ssl

import sozlukgetir

ssl._create_default_https_context = ssl._create_unverified_context

SAVEDIR = "sozluk"
os.makedirs(SAVEDIR, exist_ok=True)

wordlist_file = path.join(SAVEDIR, "tdk-autocomplete.json")
if path.exists(wordlist_file):
    with open(wordlist_file, encoding="utf-8") as fp:
        wordlist = json.load(fp)
else:
    print("Fetching word list")
    wordlist = sozlukgetir.fetch_word_list()
    with open(wordlist_file, "w", encoding="utf-8") as fp:
        json.dump(wordlist, fp, ensure_ascii=False)
        print(f"Word list saved at '{wordlist_file}'")

error_log_file = path.join(SAVEDIR, "savewords-errors.log")

successList = []
errorList = []
skippedWords = []
os.makedirs(path.join(SAVEDIR, "words"), exist_ok=True)

num_threads = 8
total_items = len(wordlist)
item_per_thread = total_items//num_threads
leftover_items = total_items - item_per_thread*num_threads

threads = []
thread_lock = threading.Lock()
active_threads = num_threads

print("Total items:", total_items)
print("Item per thread:", item_per_thread)
print("Leftover items:", leftover_items)


def progress_bar(title, done, total):
    if total == 0:
        return
    bar_length = 50
    ratio = min(done/total, 1.0)
    bar = "█"*int(bar_length*ratio) + "░"*int(bar_length*(1 - ratio))
    os.system(f"title {active_threads} thr %{(ratio*100):.3f} {title} {bar} {done}/{total}")

def update_progress():
    progress_bar("saving -",
            len(successList) + len(errorList),
            total_items)

def log_error(word, error):
    with open(error_log_file, "a", encoding="utf-8") as fp:
        fp.write(f"{word} ::\t{error}\n")

def sanitize(word: str):
    return (word
        .replace("%", "%25").replace("<", "%3C").replace(">", "%3E")
        .replace(":", "%3A").replace("\"", "%22").replace("/", "%2F")
        .replace("\\", "%5C").replace("|", "%7C").replace("?", "%3F")
        .replace("*", "%2A"))

def do_fetch(wordlist):
    global active_threads
    for i, word in enumerate(wordlist):
        time.sleep(.01)
        update_progress()
        file_path = path.join(SAVEDIR, "words", f"{sanitize(word)}.json")
        if path.exists(file_path):
            successList.append((word,))
            continue
        
        result = sozlukgetir.fetch_details(word)
        if "error" in result:    
            errorList.append((word, result["error"]))
            if result["error"] == "HTTPError" and result["code"] == 503:
                skippedWords.extend(wordlist[i:])
                print("SERVER OVERLOADED")
                with thread_lock:
                    active_threads -= 1
                sys.exit()
            elif (result["error"] == "URLError"
                    and isinstance(result["reason"], TimeoutError)):
                skippedWords.append(word)
            
            log_error(word, result)
            print(f"ERROR({word}): {result}")
        else:
            successList.append((word,))
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump(result, fp, ensure_ascii=False)


if __name__ == "__main__":
    for i in range(num_threads):
        # NOTE(bora): If items don't divide equally, leftover items
        # are added to the first thread.
        range_start = i*item_per_thread + (0 if i == 0 else leftover_items)
        range_end = (i + 1)*item_per_thread + leftover_items
        
        t = threading.Thread(target=do_fetch, args=(wordlist[range_start:range_end],))
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
    if skippedWords:
        print(f"{len(skippedWords)} WORDS SKIPPED")

    with open(error_log_file, "a", encoding="utf-8") as fp:
        if skippedWords:
            fp.write("SKIPPED WORDS::\n" + "\n".join(skippedWords))
        fp.write("\n\n")
        print(f"Error log saved: '{error_log_file}'")    
