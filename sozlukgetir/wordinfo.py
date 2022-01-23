from dataclasses import dataclass
from typing import List, Union

@dataclass
class Meaning:
    meaning: str
    is_verb: bool
    properties: List[str]

@dataclass
class Word:
    word: str
    is_proper: bool
    is_loanword: bool
    origin: Union[str, None]
    meanings: List[Meaning]
