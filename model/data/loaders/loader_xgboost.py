import pandas as pd
import numpy as np
import h5py

def load_data(cpg_path: str, mapping_path: str, step=50):

    # Load methylation data from CSV
	mapping_df = pd.read_csv(mapping_path)
	cpg_df = pd.read_csv(cpg_path)
	print(len(cpg_df.columns), len(mapping_df.index))
	# Fool-proof matching of samples
	cpg_df = cpg_df.set_index('CpG Sites').T
	mapping_df = mapping_df.set_index('sample_id')
	mapping_df = mapping_df.loc[cpg_df.index]
	# Merge data and labels
	merged = pd.concat([cpg_df, mapping_df], axis=1, join='outer')
	labels = merged['disease_state'].map({'control': 0, 'MCI': 1, "Alzheimer's": 2}).values
	data = merged.drop(columns=['disease_state', 'series_id', 'sex', 'age']).values
	print(f"Loaded dataset with {data.shape[0]} samples and {data.shape[1]} features.")
	return data[:, ::step], labels


    