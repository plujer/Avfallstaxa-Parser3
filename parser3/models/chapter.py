from dataclasses import dataclass, field
from typing import List

@dataclass
class Chapter:
    number:str
    title:str
    sections:List["Section"]=field(default_factory=list)
