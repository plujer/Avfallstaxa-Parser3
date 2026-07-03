from dataclasses import dataclass

@dataclass
class Metadata:
    row_type:str=""
    source_page:int=0
    source_style:str=""
    notes:str=""
