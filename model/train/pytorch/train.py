import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
import os

# Helpers
from model.utils.pytorch.train_loop import train_loop
from model.utils.pytorch.test_loop import test_loop
from model.utils.pytorch.cross_validate import cross_validate_model

# Import custom Dataset
from model.data.loaders.loader_pytorch import MethylationAlzheimerDataset
# Models
from model.models.pytorch.ConvNet  import ConvNet
from model.models.pytorch.RegularizedMLP import RegularizedMLP
from model.models.pytorch.SimpleMLP import SimpleMLP

if __name__ == "__main__":
	h5_path = "./model/data/train/methylation.csv"
	mapping_csv_path = "./model/data/train/idmap.csv"
	
	# Run cross validation
	results = cross_validate_model(h5_path, mapping_csv_path, batch_size=32, epochs=20, lr=1e-3, k=5)
	
	# Train final model on full dataset
	dataset = MethylationAlzheimerDataset(h5_path, mapping_csv_path)
	input_dim = dataset.data.shape[1]
	dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
	
	model = ConvNet(input_dim)
	criterion = nn.CrossEntropyLoss()
	optimizer = optim.Adam(model.parameters(), lr=1e-3)
	
	print("\nTraining final model on full dataset...")
	for epoch in range(3):
		print(f"Epoch {epoch + 1}/3")
		model = train_loop(dataloader, model, criterion, optimizer, batch_size=32)
	
	torch.save(model.state_dict(), "./model/models/pytorch/model.pkl")
	print("Model saved to ./model/models/pytorch/model.pkl")