from dataclasses import dataclass

@dataclass
class Country:
    code: int
    abbreviation: str
    full_name: str

    def __str__(self):
        return f"""{self.full_name} with code {self.code} and abbreviation {self.abbreviation}"""

    def __eq__(self, other):
        if isinstance(other, Country):
            return self.code == other.code
        elif type(other) == int:
            return self.code == other
        else:
            return False

    def __hash__(self):
        return hash(self.code)

    @staticmethod
    def prep_for_check(code: int) -> int:
        return hash(code)