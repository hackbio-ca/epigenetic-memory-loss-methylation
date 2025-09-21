import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
import os

from model.utils.pytorch.train_loop import train_loop
from model.utils.pytorch.test_loop import test_loop

# Import custom Dataset
from model.data.loaders.loader_pytorch import MethylationAlzheimerDataset
from model.models.pytorch.ConvNet  import ConvNet
from torch.utils.data import Subset
import numpy as np

def cross_validate_model(h5_path, mapping_csv_path, batch_size=32, epochs=20, lr=1e-3, k=5):

	dataset = MethylationAlzheimerDataset(h5_path, mapping_csv_path)
	input_dim = dataset.data.shape[1]
	indices = np.arange(len(dataset))
	np.random.shuffle(indices)
	fold_size = len(dataset) // k

	acc_list = []
	mse_list = []
	loss_list = []
	
	print(f"Starting {k}-Fold Cross Validation...")
	print("=" * 50)
	
	for fold in range(k):
		print(f"\nFold {fold + 1}/{k}")
		print("-" * 20)
		
		val_start = fold * fold_size
		val_end = val_start + fold_size if fold < k-1 else len(dataset)
		val_indices = indices[val_start:val_end]
		train_indices = np.concatenate([indices[:val_start], indices[val_end:]])

		train_subset = Subset(dataset, train_indices)
		val_subset = Subset(dataset, val_indices)

		train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
		val_loader = DataLoader(val_subset, batch_size=batch_size, shuffle=False)

		model = ConvNet(input_dim)
		criterion = nn.CrossEntropyLoss()
		optimizer = optim.Adam(model.parameters(), lr=lr)

		# Train
		print("Training...")
		for epoch in range(epochs):
			print(f"Epoch {epoch + 1}/{epochs}")
			model = train_loop(train_loader, model, criterion, optimizer, batch_size)

		# Validate
		print("Validating...")
		metrics = test_loop(val_loader, model, criterion, num_classes=3, 
		                   class_names=['Control', 'MCI', 'Alzheimer'])
		
		acc_list.append(metrics['accuracy'])
		mse_list.append(metrics.get('mse', 0))  # MSE no longer computed, set to 0
		loss_list.append(metrics['cross_entropy_loss'])

	print("\n" + "=" * 50)
	print("Cross Validation Results:")
	print(f"Mean Accuracy: {np.mean(acc_list):.4f} ± {np.std(acc_list):.4f}")
	print(f"Mean Loss: {np.mean(loss_list):.6f} ± {np.std(loss_list):.6f}")
	print("=" * 50)
	
	return {
		'accuracy': acc_list,
		'loss': loss_list,
		'mean_accuracy': np.mean(acc_list),
		'mean_loss': np.mean(loss_list)
	}