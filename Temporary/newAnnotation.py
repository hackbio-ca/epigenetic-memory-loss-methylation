import pandas as pd

# Load your large annotation file
annotation = pd.read_csv("infinium-methylationepic-v-1-0-b5-manifest-file.csv", skiprows=7)

# Select only the columns you want
selected_cols = [
    "IlmnID",
    "Name",
    "CHR",
    "MAPINFO",
    "UCSC_RefGene_Name",
    "UCSC_RefGene_Group"
]

# Create a new DataFrame with just these columns
filtered_annotation = annotation[selected_cols]

# Save to a new CSV
filtered_annotation.to_csv("annotation_filtered.csv", index=False)
