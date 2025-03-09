#!pip install https://huggingface.co/kormilitzin/en_core_med7_lg/resolve/main/en_core_med7_lg-any-py3-none-any.whl

import spacy
import pandas as pd


# Load the CSV file
df = pd.read_csv('./discharge.csv', dtype=str)
print(df.head())
print(df.shape)

med7 = spacy.load("en_core_med7_lg")

def extract_medical_entities(text):
    if pd.isna(text):  # Handle missing values
        return None

    doc = med7(text)  # Process text with Med7
    drugs = list(set(ent.text for ent in doc.ents if ent.label_ == "DRUG"))  # Extract unique drug names
    return "; ".join(drugs) if drugs else None  # Convert list to string for readability

# Apply the function to the 'text' column
df['extracted_drugs'] = df['text'].apply(extract_medical_entities)


# save the result
output_csv = "./extracted_drugs_med7.csv"
df[['note_id','subject_id', 'text', 'extracted_drugs']].to_csv(output_csv, index=False)


df = pd.read_csv("./annotate_id_full.csv")
ontology = {
    "ALCOHOL": ["alcohol", "alcoholic beverage", "intoxicant", "alcoholic drink", "inebriant", "ethanol", "grain alcohol", "fermentation alcohol", "ethyl alcohol", "spirits", "strong drink", "spirit", "hard liquor", "flavor", "hard drink", "booze", "liquor", "beer", "wine", "vino"],
    "DRUG": ["barbiturate", "cocaine", "cocain", "cannabis", "marihuana", "hemp", "marijuana", "ganja", "amphetamine", "pep pill", "methamphetamine", "methamphetamine hydrochloride", "meth", "deoxyephedrine", "Methedrine"],
    "OPIOID": ["heroin", "morphine", "oxycodone", "hydrocodone", "oxymorphone", "codeine", "fentanyl"],
    "NICOTINE": ["nicotine", "cigar", "cigarette", "smoke", "smoking"],
    "DRUG_ABUSE": ["drug abuse", "substance abuse", "substance misuse", "addiction"],
    "OVERDOSE": ["overdose", "OD", "drug poisoning"],
    "WITHDRAWAL": ["withdrawal", "detox", "withdrawal syndrome"]
}

df["extracted_drugs"] = df["extracted_drugs"].str.lower()
# Create new columns based on ontology dictionary with default value 0
for category in ontology.keys():
    df[category] = 0

for index, row in df.iterrows():
    extracted_text = row["extracted_drugs"]
    for category, terms in ontology.items():
        if any(term in extracted_text for term in terms):
            df.at[index, category] = 1

df.to_csv("med7_result", index=False)