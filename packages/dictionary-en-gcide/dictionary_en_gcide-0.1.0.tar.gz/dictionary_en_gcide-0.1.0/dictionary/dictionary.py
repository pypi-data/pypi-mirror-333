import json
import os
import random
from pathlib import Path

class Dictionary:
    def __init__(self, data_dir=None, lang="en"):
        """
        Initialize the dictionary with JSON files from the specified directory.
        """
        if data_dir is None:
            # Get the directory of the current module (dictionary.py)
            module_dir = Path(__file__).parent
            self.data_dir = module_dir / "data" / lang
            #self.data_dir = Path(pkg_resources.resource_filename("dictionary", "data/en"))
        else:
            self.data_dir = Path(data_dir)
        #print(f"Current working directory: {os.getcwd()}")
        self.entries = self._load_entries()

    def _load_entries(self):
        """
        Load dictionary entries from JSON files in the data directory.
        """
        entries = {}
        #print(f"Loading data from: {self.data_dir}")  # Debug print
        for file_path in self.data_dir.glob("words_*.json"):
            with open(file_path, "r") as f:
                data = json.load(f)
                #print(f"Loaded {len(data)} entries from {file_path}")  # Debug print
                for entry in data:
                    worddic = data.get(entry)
                    entries[entry] = worddic
        #print(f"Total entries loaded: {len(entries)}")  # Debug print
        return entries
    
    def randomWord(self):
        """
        Return the value of a random word
        """
        return random.choice(list(self.entries.values()))

    def lookup(self, word):
        """
        Look up a word in the dictionary.
        """
        word = word.lower()
        return self.entries.get(word, None)

# Example usage
if __name__ == "__main__":
    dictionary = Dictionary()
    result = dictionary.lookup("truth")
    print(result)