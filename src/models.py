from dataclasses import dataclass 
from typing import List, Tuple
from src.exceptions import InvalidMatchDataError

@dataclass
class Match:
    match_id: str
    date: str
    map_name: str
    kills: int
    deaths: int
    assists: int
    result: str

    #Validate input data
    def __post_init__(self):
        if self.kills < 0 or self.deaths < 0 or self.assists < 0:
            raise InvalidMatchDataError(f"Stats cannot be negative in match {self.match_id}")
        if self.result not in ("WIN", "LOSS"):
            raise InvalidMatchDataError(f"Invalid match result: {self.result}")

    @property
    def is_win(self) -> bool:
        return self.result == "WIN"

    #Calculate K/D ratio with zero division protection
    @property
    def kd_ratio(self) -> float:
        if self.kills == 0:
            return float(self.kills)
        return round(self.kills / self.deaths, 2)

    #Return K/D/A as a tuple
    def get_kda_tuple(self) -> Tuple[int, int, int]:
        return (self.kills, self.deaths, self.assists)

class Player:
    def __init__(self, nickname: str):
        self.nickname: str = nickname
        self.matches: List[Match] = []

    def add_match(self, match: Match) -> None:
        self.matches.append(match)

    def total_matches(self) -> int:
        return len(self.matches)