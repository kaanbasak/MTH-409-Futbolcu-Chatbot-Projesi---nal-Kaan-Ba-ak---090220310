import pandas as pd
import os

class DataLoader:
    def __init__(self, csv_path='data/top5_leagues_player.csv'):
        """
        Initializes the DataLoader by loading the CSV file into a pandas DataFrame.
        """
        self.csv_path = csv_path
        self.df = self._load_data()

    def _load_data(self):
        """
        Loads data from the CSV file. Handles FileNotFoundError.
        """
        if not os.path.exists(self.csv_path):
            print(f"Error: The file {self.csv_path} was not found.")
            return None
        
        try:
            df = pd.read_csv(self.csv_path)
            # Ensure string columns are treated as strings to avoid errors during search
            df['name'] = df['name'].fillna('').astype(str)
            df['full_name'] = df['full_name'].fillna('').astype(str)
            return df
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None

    def get_player_info(self, player_name):
        """
        Searches for a player by name (case-insensitive, partial match).
        Returns a dictionary of player info if found, else None.
        """
        if self.df is None:
            return None

        player_name = player_name.strip().lower()
        if not player_name:
            return None

        # Search in 'name' or 'full_name'
        # We look for the first match that contains the search term
        mask = (
            self.df['name'].str.lower().str.contains(player_name, na=False) | 
            self.df['full_name'].str.lower().str.contains(player_name, na=False)
        )
        
        results = self.df[mask]

        if results.empty:
            return None
        
        # Taking the first match for simplicity
        player_row = results.iloc[0]

        # Constructing the dictionary based on available columns
        return self._format_player_info(player_row)

    def find_player_in_text(self, text):
        """
        Iterates through the database to find if any player's name exists in the text.
        Returns the player info dictionary if found, else None.
        """
        if self.df is None or not text:
            return None
        
        text = text.lower()
        
        # We need to prioritize longer matches (e.g. 'Kevin De Bruyne' over 'Kevin')
        # So we can try to find matches. 
        # Since iterating 3000 rows is fast in Python, we can do it.
        
        # Create a list of (name, full_name, row_index)
        # It's better to verify if any name in DB is substring of text.
        
        for index, row in self.df.iterrows():
            name = str(row['name']).lower()
            full_name = str(row['full_name']).lower()
            
            # Check if name is in text (and is not too short to avoid false positives like 'Ed')
            if (len(name) > 3 and name in text) or (len(full_name) > 3 and full_name in text):
                return self._format_player_info(row)
                
        return None

    def _format_player_info(self, player_row):
        # Constructing the dictionary based on available columns
        player_info = {
            "name": player_row.get('name', 'N/A'),
            "full_name": player_row.get('full_name', 'N/A'),
            "age": str(player_row.get('age', 'N/A')),
            "position": player_row.get('position', 'N/A'),
            "club": player_row.get('club', 'N/A'),
            "league": player_row.get('league', 'N/A'),
            "nationality": player_row.get('nationality', 'N/A'),
            "price": str(player_row.get('price', 'N/A')) + " M€" if pd.notna(player_row.get('price')) else "N/A"
        }
        return player_info

