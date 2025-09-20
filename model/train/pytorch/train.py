import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
import os

from model.utils.pytorch.train_loop import train_loop
from model.utils.pytorch.test_loop import test_loop

# Import custom Dataset
from model.data.loaders.loader_pytorch import MethylationAlzheimerDataset
from model.models.pytorch.model  import NeuralNet

def cross_validate_model(h5_path, mapping_csv_path, batch_size=32, epochs=3, lr=1e-3, k=5):
	from torch.utils.data import Subset
	import numpy as np

	dataset = MethylationAlzheimerDataset(h5_path, mapping_csv_path)
	input_dim = dataset.data.shape[1]
	indices = np.arange(len(dataset))
	np.random.shuffle(indices)
	fold_size = len(dataset) // k

	acc_list = []
	for fold in range(k):
		val_start = fold * fold_size
		val_end = val_start + fold_size if fold < k-1 else len(dataset)
		val_indices = indices[val_start:val_end]
		train_indices = np.concatenate([indices[:val_start], indices[val_end:]])

		train_subset = Subset(dataset, train_indices)
		val_subset = Subset(dataset, val_indices)

		train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
		val_loader = DataLoader(val_subset, batch_size=batch_size, shuffle=False)

		model = NeuralNet(input_dim)
		criterion = nn.CrossEntropyLoss()
		optimizer = optim.Adam(model.parameters(), lr=lr)

		# Train
		train_loop(train_loader, model, criterion, optimizer, batch_size)

		# Validate
		test_loop(val_loader, model, criterion)

	print(f"Mean CV Accuracy: {np.mean(acc_list):.4f} ± {np.std(acc_list):.4f}")
	return acc_list

def train_model(h5_path, mapping_csv_path, batch_size=32, epochs=3, lr=1e-3):
	# Load dataset
	dataset = MethylationAlzheimerDataset(h5_path, mapping_csv_path)
	dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
	input_dim = dataset.data.shape[1]

	# Initialize model, loss, optimizer
	model = NeuralNet(input_dim)
	criterion = nn.CrossEntropyLoss()
	optimizer = optim.Adam(model.parameters(), lr=lr)

	# Training loop
	for epoch in range(epochs):
		print("Epoch {}/{}".format(epoch+1, epochs), end='\r')
		train_loop(dataloader, model, criterion, optimizer, batch_size)


	print("Training complete.")
	return model

if __name__ == "__main__":
	h5_path = "./model/data/train/methylation.csv"
	mapping_csv_path = "./model/data/train/idmap.csv"
	# Run cross-validation
	# cross_validate_model(h5_path, mapping_csv_path, batch_size=32, epochs=3, lr=1e-3, k=5)
	# Or run standard training
	model = train_model(h5_path, mapping_csv_path, batch_size=32, epochs=10, lr=1e-3)
	torch.save(model.state_dict(), "./model/models/pytorch/model.pkl")