import requests
import pandas as pd

# API endpoint URL
api_url = "https://fantasy.premierleague.com/api/leagues-classic/1546610/standings/"

def fetch_fpl_data(api_url):
    """Fetches data from the FPL API."""
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from API. Status code: {response.status_code}")

def process_fpl_data(data, paid_players):
    """Processes the FPL data, filters for paid players, cleans columns, and returns a DataFrame."""
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

    # Rename index column
    filtered_df = filtered_df.rename_axis("Rank")

    return filtered_df

def main():
    # List of paid player entry IDs
    paid_players = [
        7027454, 1535831, 2457808, 7071443, 227445, 735686,
        2515831, 4461725, 4642573, 4489873, 775920, 384349,
        4173520, 2518553, 6895049, 3043941, 4196774
    ]

    try:
        # Fetch data from API
        data = fetch_fpl_data(api_url)

        # Process data to filter and clean
        filtered_df = process_fpl_data(data, paid_players)

        # Save the filtered data to a CSV file (optional)
        filtered_df.to_csv("filtered_fpl_league_standings.csv", index=False)

        # Save the filtered data to a JSON file
        filtered_df.to_json("fpl_standings.json", orient="records", indent=4)

        print("Filtered data successfully created and saved to 'fpl_standings.json'")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()