# Custom PyTorch Dataset for methylation data and Alzheimer's disease label
import torch
from torch.utils.data import Dataset
import pandas as pd
import h5py
import numpy as np
import os, warnings
warnings.filterwarnings("ignore")

class MethylationAlzheimerDataset(Dataset):

	def __init__(self, cpg_path, mapping_path, step=50):

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
		self.labels = merged['disease_state'].map({'control': 0, 'MCI': 1, "Alzheimer's": 2}).values
		self.data = merged.drop(columns=['disease_state', 'series_id', 'sex', 'age']).values[:, ::step]
		print(f"Loaded dataset with {self.data.shape[0]} samples and {self.data.shape[1]} features.")
		
		


	def __len__(self):
		return len(self.data)

	def __getitem__(self, idx):
		# Return methylation data and binary label as tensors
		x = torch.tensor(self.data[idx], dtype=torch.float32)
		y = torch.tensor(self.labels[idx], dtype=torch.long)
		return x, y

if __name__ == "__main__":
    # Example usage
    dataset = MethylationAlzheimerDataset(
        cpg_path='./model/data/train/methylation.csv',
        mapping_path='./model/data/train/idmap.csv'
    )
    print(f"Dataset size: {len(dataset)}")
    sample_x, sample_y = dataset[0]
    print(f"Sample data shape: {sample_x.shape}, Sample label: {sample_y}")