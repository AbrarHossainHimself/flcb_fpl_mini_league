import requests
import pandas as pd
import json
from datetime import datetime

# API endpoint URL
api_url = "https://fantasy.premierleague.com/api/leagues-classic/1546610/standings/"

def fetch_fpl_data(api_url):
    """Fetches data from the FPL API."""
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        raise

def process_fpl_data(data, paid_players):
    """Processes the FPL data and returns a DataFrame."""
    try:
        # Extract standings data
        standings = data["standings"]["results"]
        
        # Convert to DataFrame
        df = pd.DataFrame(standings)
        
        # Filter for paid players
        filtered_df = df[df['entry'].isin(paid_players)]
        
        # Clean and format
        filtered_df = filtered_df.drop(columns=[
            'id', 'entry', 'has_played', 'last_rank', 'rank_sort', 'rank'
        ])
        
        # Rename columns
        filtered_df = filtered_df.rename(columns={
            'event_total': 'GW Total',
            'player_name': 'Player',
            'entry_name': 'Team',
            'total': 'Total Points'
        })
        
        # Sort by total points
        filtered_df = filtered_df.sort_values('Total Points', ascending=False)
        
        return filtered_df[['Player', 'Team', 'GW Total', 'Total Points']]
        
    except Exception as e:
        print(f"Error processing data: {e}")
        raise

def save_data(df):
    """Saves the data to both JSON and CSV files."""
    try:
        # Save to JSON with timestamp
        json_data = {
            'last_updated': datetime.utcnow().isoformat(),
            'data': json.loads(df.to_json(orient='records'))
        }
        
        with open('fpl_standings.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
            
        # Save to CSV
        df.to_csv('filtered_fpl_league_standings.csv', index=False)
        
        print("Data successfully saved to files")
        
    except Exception as e:
        print(f"Error saving data: {e}")
        raise

def main():
    paid_players = [
        7027454, 1535831, 2457808, 227445, 735686,
        2515831, 4461725, 4642573, 4489873, 775920, 384349,
        4173520, 2518553, 6895049, 3043941, 4196774, 2334753
    ]
    
    try:
        # Fetch and process data
        raw_data = fetch_fpl_data(api_url)
        df = process_fpl_data(raw_data, paid_players)
        save_data(df)
        return 0
    except Exception as e:
        print(f"Failed to update data: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
