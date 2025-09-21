import pandas as pd
import numpy as np
import h5py

def load_data(cpg_path: str, mapping_path: str, indices: tuple[int,int]=[1000,5000]):

    # Load methylation data from CSV
	mapping_df = pd.read_csv(mapping_path)
	cpg_df = pd.read_csv(cpg_path)
	print(len(cpg_df.columns), len(mapping_df.index))
	# Fool-proof matching of samples
	cpg_df = cpg_df.set_index(cpg_df.columns.values[0]).T
	mapping_df = mapping_df.set_index('sample_id')
	mapping_df = mapping_df.loc[cpg_df.index]
	# Merge data and labels
	merged = pd.concat([cpg_df, mapping_df], axis=1, join='outer')
	labels = merged['disease_state'].map({'control': 0, 'MCI': 1, "Alzheimer's": 2}).values
	data = merged.drop(columns=['disease_state', 'series_id', 'sex', 'age']).values
	print(f"Loaded dataset with {data.shape[0]} samples and {data.shape[1]} features.")
	
	i_spl, i_ft = indices
	i_spl, i_ft = min(i_spl, data.shape[0]), min(i_ft, data.shape[1])
	return data[:, :i_ft], labels[:i_spl]

def load_data_h5(h5_path: str, mapping_path: str, indices: tuple[int,int]=[1000,5000]):

	# Load methylation data from H5
	mapping_df = pd.read_csv(mapping_path)
	with h5py.File(h5_path, 'r') as h5f:
		data = h5f['data'][:]
	print(f"Loaded dataset with {data.shape[0]} samples and {data.shape[1]} features.")
	labels = mapping_df['disease_state'].map({'control': 0, 'MCI': 1, "Alzheimer's": 2}).values
	# Return full data if no indices provided
	if indices is None: 
		return data, labels
	# Slice data if indices provided
	i_spl, i_ft = indices
	i_spl, i_ft = min(i_spl, data.shape[0]), min(i_ft, data.shape[1])
	return data[:i_spl, :i_ft], labels[:i_spl]

if __name__ == "__main__":
	# Example usage
	mapping_path = './model/data/train/idmap.csv'
	# .csv
	# cpg_path = './model/data/train/methylation.csv'
	# data, labels = load_data(cpg_path, mapping_path)
	# print(f"Data shape: {data.shape}, Labels shape: {labels.shape}")
	# .h5
	h5_path = './model/data/train/methylation.h5'
	data_h5, labels_h5 = load_data_h5(h5_path, mapping_path)
	print(f"Data shape: {data_h5.shape}, Labels shape: {labels_h5.shape}")