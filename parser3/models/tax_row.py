from dataclasses import dataclass

@dataclass
class TaxRow:
    chapter:str=""
    section:str=""
    group:str=""
    name:str=""
    variant:str=""
    unit:str=""
    price:str=""
    ewc:str=""
    un_number:str=""
    export:bool=True
