import json
import re
from typing import Iterator, List
from src.models import Match
from src.exceptions import InvalidMatchDataError

#Regex pattern to extract data from a raw log string
LOG_PATTERN = re.compile(
    r"\[(?P<date>.*?)\] MAP: (?P<map>\w+) \| K: (?P<k>\d+) D: (?P<d>\d+) A: (?P<a>\d+) \| RES: (?P<res>WIN|LOSS)"
)

#Parse a single text log line using regular expressions
def parse_log_line(match_id: str, line: str) -> Match:
    parsed = LOG_PATTERN.search(line)
    if not parsed:
        raise InvalidMatchDataError(f"Log line format is invalid: {line.strip()}")

    return Match(
        match_id=match_id,
        date=parsed.group("date"),
        map_name=parsed.group("map"),
        kills=int(parsed.group("k")),
        deaths=int(parsed.group("d")),
        assists=int(parsed.group("a")),
        result=parsed.group("res")
    )

#Generator to read log files line by line without memory overload
def generate_matches_from_log(file_path: str) -> Iterator[Match]:
    with open(file_path, "r", encoding="utf-8") as file_obj:
        for index, line in enumerate(file_obj, start=1):
            if line.strip():
                yield parse_log_line(f"log_{index}", line)

#Load and instantiate Match objects from a JSON file
def load_matches_from_json(file_path: str) -> List[Match]:
    with open(file_path, "r", encoding="utf-8") as file_obj:
        data = json.load(file_obj)

    matches = []
    for item in data:
        matches.append(Match(
            match_id=item["match_id"],
            date=item["date"],
            map_name=item["map"],
            kills=item["kills"],
            deaths=item["deaths"],
            assists=item["assists"],
            result=item["result"]
        ))
    return matches