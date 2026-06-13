from dataclasses import dataclass

from database.Country import Country


@dataclass
class Contiguity:
    """
    Represents a contiguity between 2 states with the given type
    """
    country_code_a: int
    country_code_b: int

    country_a: Country
    country_b: Country

    def __eq__(self, other):
        return tuple([self.country_code_a, self.country_code_b]) == tuple([other.country_code_a, other.country_code_b])