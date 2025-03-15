import pandas as pd
import re

# Load your input CSV file (adjust the filename as needed)
df = pd.read_csv("merged_all.csv")

# Function to extract labels from the 'entities' string
def extract_labels(entities_str):
    if pd.isnull(entities_str):
        return []
    # This regex finds any text inside parentheses
    return re.findall(r'\((.*?)\)', entities_str)

# Mapping from your entity labels to the desired column names in the summary table.
# Note: 'ALCOHOL' will become 'Alcohol' while others remain uppercase or get a space.
label_map = {
    "ALCOHOL": "Alcohol",
    "DRUG": "DRUG",
    "OPIOID": "OPIOID",
    "NICOTINE": "NICOTINE",
    "DRUG_ABUSE": "DRUG ABUSE",
    "OVERDOSE": "OVERDOSE",
    "WITHDRAWAL": "WITHDRAWAL"
}

# Initialize the summary DataFrame with the note_id column
summary_df = pd.DataFrame()
summary_df["note_id"] = df["note_id"]

# For each label, create a binary column
for key, col_name in label_map.items():
    summary_df[col_name] = df["entities"].apply(lambda x: 1 if key in extract_labels(x) else 0)

# Save the resulting summary table to a new CSV file
summary_df.to_csv("OntoNER_summary_table.csv", index=False)
