import os
import sys
import time
from src.models import Match, Player
from src.parsers import load_matches_from_json, generate_matches_from_log
from src.analytics import PlayerAnalytics
from src.exceptions import CS2TrackerError
from src.database import DatabaseManager

#Helper function to print formatted player statistics
def display_analytics(player: Player) -> None:
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

#Simulate fetching data from real API like FACEIT
def fetch_mock_api_data() -> list[Match]:
    print("Fetching data from API...")
    time.sleep(1.5) #Simulate network delay
    return [
        Match("api_1", "2026-10-25 10:00:00", "de_nuke", 18, 15, 4, "WIN"),
        Match("api_2", "2026-10-25 11:30:00", "de_ancient", 22, 10, 7, "WIN"),
        Match("api_3", "2026-10-25 13:00:00", "de_vertigo", 14, 20, 3, "LOSS")
    ]

#Main CLI entry point for CS2 Analytics application
def main() -> None:
    db = DatabaseManager()
    
    #Define paths to data sources 
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "data", "mock_matches.json")
    log_path = os.path.join(base_dir, "data", "game_logs.log")

    while True:
        print("\n=== CS2 Analytics CLI Tracker ===")
        print("1. Analyze Local Mock Data (Offline Backup)")
        print("2. Fetch & Sync Data from API (Simulated)")
        print("3. Analyze API Data from Database")
        print("4. Clear API Database Cache")
        print("5. Exit")
        print("===================================")  

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            player = Player(nickname="OfflineUser")
            #Loading local data
            try:
                if os.path.exists(json_path):
                    for match in load_matches_from_json(json_path):
                        player.add_match(match)
                if os.path.exists(log_path):
                    for match in generate_matches_from_log(log_path):
                        player.add_match(match)
                display_analytics(player)
            except CS2TrackerError as e:
                print(f"[ERROR] Loading local data failed: {e}")

        elif choice == "2":
            api_matches = fetch_mock_api_data()
            db.save_matches(api_matches)
            print(f"[SUCCESS] Saved {len(api_matches)} matches from API to database")

        elif choice == "3":
            player = Player(nickname="APIUser")
            db_matches = db.load_matches()
            for match in db_matches:
                player.add_match(match)
            display_analytics(player)

        elif choice == "4":
            db.clear_database()
            print("[INFO] Database cache cleared successfully")

        elif choice == "5":
            print("Exiting... Good luck on the servers!")
            sys.exit(0)
        else:
            print("[ERROR] Invalid choice. Please select 1-5")

if __name__ == "__main__":
    main()
