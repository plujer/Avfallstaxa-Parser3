from dataclasses import dataclass, field
from typing import List

@dataclass
class Section:
    number:str
    title:str
    groups:List[str]=field(default_factory=list)
    tables:List["Table"]=field(default_factory=list)
