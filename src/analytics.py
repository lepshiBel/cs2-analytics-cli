from typing import Dict, Optional
from src.models import Player

#Class responsible for calculating player statistics
class PlayerAnalytics:
    def __init__(self, player: Player):
        self.player = player
        self.matches = player.matches

    #Calculates the win rate percentage
    def calculate_win_rate(self) -> float:
        if not self.matches:
            return 0.0
        wins = sum(1 for match in self.matches if match.is_win)
        return round((wins / len(self.matches)) * 100, 2)

    #Calculate the average K/D ratio across all matches
    def calculate_average_kd(self) -> float:
        if not self.matches:
            return 0.0
        total_kd = sum(match.kd_ratio for match in self.matches)
        return round(total_kd / len(self.matches), 2)

    #Determine the best map based on the number of wins
    def get_best_map(self) -> Optional[str]:
        if not self.matches:
            return None

        map_wins: Dict[str, int] = {}
        for match in self.matches:
            if match.is_win:
                map_wins[match.map_name] = map_wins.get(match.map_name, 0) + 1
        
        if not map_wins:
            return None

        best_map = sorted(map_wins.items(), key=lambda item: item[1], reverse=True)[0][0]
        return best_map