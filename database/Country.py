from dataclasses import dataclass

@dataclass
class Country:
    code: int
    abbreviation: str
    full_name: str

    def __str__(self):
        return f"""{self.full_name} with code {self.code} and abbreviation {self.abbreviation}"""

    def __eq__(self, other):
        return self.code == other.code