from dataclasses import dataclass

@dataclass
class SemanticContext:
    chapter: str = ""
    section: str = ""
    section_title: str = ""
    group: str = ""
    header: str = ""
