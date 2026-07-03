from dataclasses import dataclass, field
from typing import List

@dataclass
class Table:
    title:str=""
    rows:List["TaxRow"]=field(default_factory=list)
