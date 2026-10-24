import os
from src.models import Player
from src.parsers import load_matches_from_json, generate_matches_from_log
from src.analytics import PlayerAnalytics
from src.exceptions import CS2TrackerError

#Main CLI entry point for CS2 Analytics application
def main() -> None:
    print("=== CS2 Analytics CLI Tracker ===")

    player_name = input("Enter player nickname: ").strip() or "DefaultPlayer"
    player = Player(nickname=player_name)

    #Define paths to data sources 
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "data", "mock_matches.json")
    log_path = os.path.join(base_dir, "data", "game_logs.log")

    #Load matches from JSON
    try:
        if os.path.exists(json_path):
            json_matches = load_matches_from_json(json_path)
            for match in json_matches:
                player.add_match(match)
            print(f"[INFO] Loaded {len(json_matches)} matches from JSON")
    except CS2TrackerError as e:
        print(f"[ERROR] JSON loading failed: {e}")

    #Load matches from Log file using generator
    try:
        if os.path.exists(log_path):
            log_matches_count = 0
            for match in generate_matches_from_log(log_path):
                player.add_match(match)
                log_matches_count += 1
            print(f"[INFO] Loaded {log_matches_count} matches from log generator")
    except CS2TrackerError as e:
        print(f"[ERROR] Log parsing failed: {e}")

    #Display analytics
    if player.total_matches() == 0:
        print(f"[WARNING] No match data available for analysis")
        return

    analytics = PlayerAnalytics(player)

    print("\n" + "="*30)
    print(f"STATS FOR PLAYER: {player.nickname.upper()}")
    print("="*30)
    print(f"Total Matches Played : {player.total_matches()}")
    print(f"Win Rate             : {analytics.calculate_win_rate()}%")
    print(f"Average K/D Ratio    : {analytics.calculate_average_kd()}")
    print(f"Best Map             : {analytics.get_best_map() or "N/A"}")
    print("="*30)

if __name__ == "__main__":
    main()
