#!/usr/bin/env python3
import os
import pandas as pd
import zipfile

# List to store DataFrames for all entity results
all_dfs = []

# Process sub files (original entity files)
for i in range(1, 31):
    all_file = f"sub_{i}_with_entities.csv"
    if os.path.exists(all_file):
        df = pd.read_csv(all_file)
        df["source_file"] = all_file  # Track the source file
        all_dfs.append(df)
    else:
        print(f"File {all_file} does not exist, skipping.")

# Add sup_NER_res.csv to the list
sup_file = "sup_NER_res.csv"
if os.path.exists(sup_file):
    sup_df = pd.read_csv(sup_file)
    sup_df["source_file"] = sup_file  # Track the source file
    all_dfs.append(sup_df)
else:
    print(f"File {sup_file} does not exist, skipping.")

# Merge all files into one DataFrame
if all_dfs:
    merged_all = pd.concat(all_dfs, ignore_index=True)
    merged_all_filename = "merged_all.csv"
    merged_all.to_csv(merged_all_filename, index=False)
    print(f"Saved merged all results to: {merged_all_filename}")
else:
    print("No files to merge for merged_all.csv")
    exit()

# Now apply filtering on the merged_all DataFrame
# For example, here we keep rows with non-empty 'entities'
merged_filtered = merged_all[ merged_all['entities'].notna() & (merged_all['entities'].str.strip() != "") ]
merged_filtered_filename = "merged_filtered.csv"
merged_filtered.to_csv(merged_filtered_filename, index=False)
print(f"Saved filtered results to: {merged_filtered_filename}")
