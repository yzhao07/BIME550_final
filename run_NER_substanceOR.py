#!/usr/bin/env python3
import os
import pandas as pd
import spacy
from spacy.pipeline import EntityRuler
from nltk.corpus import wordnet as wn
import nltk

# Uncomment if needed to download WordNet data
# nltk.download('wordnet')

def get_synonyms(term):
    """Retrieve synonyms for a given term using WordNet."""
    synonyms = set()
    for syn in wn.synsets(term):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    synonyms.discard(term)
    return list(synonyms)

def build_nlp_pipeline():
    """Set up the spaCy NLP pipeline with a custom EntityRuler using your ontology."""
    # Define your ontology
    ontology = {
    "ALCOHOL": ["alcohol", "alcoholic beverage", "intoxicant", "alcoholic drink", "inebriant", "ethanol", "grain alcohol", "fermentation alcohol", "ethyl alcohol", "spirits", "strong drink", "spirit", "hard liquor", "flavor", "hard drink", "booze", "liquor", "beer", "wine", "vino"],
    "DRUG": ["barbiturate", "cocaine", "cocain", "cannabis", "marihuana", "hemp", "marijuana", "ganja", "amphetamine", "pep pill", "methamphetamine", "methamphetamine hydrochloride", "meth", "deoxyephedrine", "Methedrine"],
    "OPIOID": ["heroin", "morphine", "oxycodone", "hydrocodone", "oxymorphone", "codeine", "fentanyl"],
    "NICOTINE": ["nicotine", "cigar", "cigarette", "smoke", "smoking"],
    "DRUG_ABUSE": ["drug abuse", "substance abuse", "substance misuse", "addiction"],
    "OVERDOSE": ["overdose", "OD", "drug poisoning"],
    "WITHDRAWAL": ["withdrawal", "detox", "withdrawal syndrome"]
    }
    # Expand the ontology with synonyms from WordNet
    # expanded_ontology = {
    #     cat: list(set(terms) | {syn for term in terms for syn in get_synonyms(term)})
    #     for cat, terms in ontology.items()
    # }
    
    # Load spaCy model and create a pipeline with only the custom EntityRuler
    nlp = spacy.load("en_core_web_sm")
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = []
    for category, synonyms in ontology.items():
        for synonym in synonyms:
            token_pattern = [{"LOWER": token.lower()} for token in synonym.split()]
            patterns.append({"label": category, "pattern": token_pattern})
    ruler.add_patterns(patterns)
    
    # Remove the default NER so only custom detections are used
    if "ner" in nlp.pipe_names:
        nlp.remove_pipe("ner")
    
    return nlp

def extract_entities(nlp, text):
    """Process a text and extract custom entities as a string."""
    doc = nlp(text)
    return ", ".join(f"{ent.text} ({ent.label_})" for ent in doc.ents)

def process_file(nlp, infile, outfile):
    """Load a CSV file, process its 'text' column, add entities, and save the result."""
    print(f"Processing {infile} ...")
    df = pd.read_csv(infile)
    # Apply extraction on the 'text' column (adjust the column name if needed)
    df['entities'] = df['text'].apply(lambda x: extract_entities(nlp, x) if isinstance(x, str) else "")
    df.to_csv(outfile, index=False)
    print(f"Saved results to {outfile}")

def main():
    nlp = build_nlp_pipeline()
    # Process files sub_1.csv to sub_31.csv
    for i in range(1, 31):
        infile = f"sub_{i}.csv"
        outfile = f"sub_{i}_with_entities.csv"
        if os.path.exists(infile):
            process_file(nlp, infile, outfile)
        else:
            print(f"File {infile} does not exist, skipping.")

if __name__ == "__main__":
    main()


