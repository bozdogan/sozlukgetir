# Sözlükgetir Dictionary Crawler

Sözlükgetir is a crawler/fetcher for the Turkish Language Association's[^1] online Turkish dictionary[^2].

I plan to add support for alternative dictionaries for Turkish language
(Wictionary/Vikisözlük).

[^1]: _tr._ Türk Dil Kurumu (TDK), [official website](https://www.tdk.gov.tr/)
[^2]: Current Turkish Dictionary (_tr._ Güncel Türkçe Sözlük), [link](https://sozluk.gov.tr/)


## Dependencies

None other than Python!


## API Reference

### `fetch_word_list`
Fetches available words for querying from the dictionary website.

_e.g._
```python
import sozlukgetir

print("Fetching word list")
wordList = sozlukgetir.fetch_word_list()

print("WORDS: ", ", ".join(wordList))  # Approximately 96k words
```

### `fetch_details(word: str)`
Fetches details of one word including its different meanings and spelling.

_e.g._
```python
import sozlukgetir

print(sozlukgetir.fetch_details("çıkmak"))
```
