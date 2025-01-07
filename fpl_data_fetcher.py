import requests
import pandas as pd
import json
import os
from datetime import datetime

# API endpoint URL
api_url = "https://fantasy.premierleague.com/api/leagues-classic/1546610/standings/"

def fetch_fpl_data(api_url):
    """Fetches data from the FPL API."""
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def process_fpl_data(data, paid_players):
    """Processes the FPL data, filters for paid players, cleans columns, and returns a DataFrame."""
    if not data:
        return None
        
    try:
        # Extract standings data
        standings = data["standings"]["results"]

        # Convert standings to DataFrame
        df = pd.DataFrame(standings)

        # Filter for paid players
        filtered_df = df[df['entry'].isin(paid_players)]

        # Drop unnecessary columns
        filtered_df = filtered_df.drop(columns=['id', 'entry', 'has_played', 'last_rank', 'rank_sort', 'rank'])

        # Rename columns
        filtered_df = filtered_df.rename(columns={
            'event_total': 'GW Total',
            'player_name': 'Player',
            'entry_name': 'Team',
            'total': 'Total Points'
        })

        # Reorder columns
        filtered_df = filtered_df[['Player', 'Team', 'GW Total', 'Total Points']]

        # Sort by Total Points in descending order
        filtered_df = filtered_df.sort_values('Total Points', ascending=False)

        return filtered_df

    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def save_data(df, json_file, csv_file):
    """Saves the DataFrame to both JSON and CSV files."""
    if df is None:
        return False
        
    try:
        # Save to JSON with timestamp
        data_with_timestamp = {
            'last_updated': datetime.now().isoformat(),
            'data': json.loads(df.to_json(orient='records'))
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data_with_timestamp, f, indent=2, ensure_ascii=False)
            
        # Save to CSV
        df.to_csv(csv_file, index=False)
        return True
        
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def main():
    # List of paid player entry IDs
    paid_players = [
        7027454, 1535831, 2457808, 7071443, 227445, 735686,
        2515831, 4461725, 4642573, 4489873, 775920, 384349,
        4173520, 2518553, 6895049, 3043941, 4196774
    ]

    # Fetch and process data
    raw_data = fetch_fpl_data(api_url)
    if raw_data:
        processed_df = process_fpl_data(raw_data, paid_players)
        if processed_df is not None:
            success = save_data(
                processed_df,
                'fpl_standings.json',
                'filtered_fpl_league_standings.csv'
            )
            if success:
                print("Data successfully updated and saved")
                return 0
    
    print("Failed to update data")
    return 1

if __name__ == "__main__":
    exit(main())