import sozlukgetir
import ssl

if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    print("Fetching autocomplete word list")
    wordList = sozlukgetir.fetch_word_list()

    print("WORDS::\n")
    print(", ".join(wordList[:20]) + "\n  ...\n" + ", ".join(wordList[-10:]))
    print()
    
    word_cikmak = sozlukgetir.fetch_details(wordList[19049])
    print(word_cikmak)
