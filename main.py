import os
import sys
import time
from src.models import Player
from src.parsers import load_matches_from_json, generate_matches_from_log
from src.analytics import PlayerAnalytics
from src.exceptions import CS2TrackerError
from src.database import DatabaseManager

#Helper function to print formatted player statistics
def display_analytics(player: Player) -> None:
    if player.total_matches() == 0:
        print("\n[WARNING] No match data available for analysis.")
        return

    analytics = PlayerAnalytics(player)
    print("\n" + "="*30)
    print(f" STATS FOR PLAYER: {player.nickname.upper()} ")
    print("="*30)
    print(f"Total Matches Played : {player.total_matches()}")
    print(f"Win Rate             : {analytics.calculate_win_rate()}%")
    print(f"Average K/D Ratio    : {analytics.calculate_average_kd()}")
    print(f"Best Map             : {analytics.get_best_map() or 'N/A'}")
    print("="*30)

def main() -> None:
    db = DatabaseManager()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    json_path = os.path.join(base_dir, "data", "mock_matches.json")
    log_path = os.path.join(base_dir, "data", "game_logs.log")
    external_path = os.path.join(base_dir, "data", "external_matches.json")

    while True:
        print("\n=== CS2 ANALYTICS CLI ===")
        print("1. Analyze Offline Local Backup (JSON + Logs)")
        print("2. Sync External Matches to SQLite Database")
        print("3. Analyze Database Matches")
        print("4. Clear Database Cache")
        print("5. Exit")
        print("=========================")
        
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            player = Player(nickname="OfflineUser")
            try:
                if os.path.exists(json_path):
                    for m in load_matches_from_json(json_path):
                        player.add_match(m)
                if os.path.exists(log_path):
                    for m in generate_matches_from_log(log_path):
                        player.add_match(m)
                display_analytics(player)
            except CS2TrackerError as e:
                print(f"[ERROR] Loading offline data failed: {e}")

        elif choice == "2":
            try:
                if os.path.exists(external_path):
                    print("Syncing data to SQLite database...")
                    time.sleep(1)
                    matches_to_sync = load_matches_from_json(external_path)
                    db.save_matches(matches_to_sync)
                    print(f"[SUCCESS] Synced {len(matches_to_sync)} matches into SQLite database.")
                else:
                    print("[ERROR] External dataset file not found.")
            except CS2TrackerError as e:
                print(f"[ERROR] Sync failed: {e}")

        elif choice == "3":
            player = Player(nickname="DatabaseUser")
            db_matches = db.load_matches()
            for m in db_matches:
                player.add_match(m)
            display_analytics(player)

        elif choice == "4":
            db.clear_database()
            print("[INFO] Database cache cleared successfully.")

        elif choice == "5":
            print("Exiting... Good luck on the servers!")
            sys.exit(0)
        else:
            print("[ERROR] Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()