
# PyTorch Neural Network Template for Methylation Alzheimer's Dataset
import torch
import torch.nn as nn

class NeuralNet(nn.Module):
	def __init__(self, input_dim, hidden_dim=128, output_dim=3):
		super(NeuralNet, self).__init__()
		# self.conv1 = nn.Conv1d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
		# self.pool = nn.MaxPool1d(kernel_size=2)
		# self.relu = nn.ReLU()
		# self.dropout = nn.Dropout(0.2)
		# # After pooling, input_dim // 2 features per channel
		# self.fc1 = nn.Linear(16 * (input_dim // 2), hidden_dim)
		# self.fc2 = nn.Linear(hidden_dim, output_dim)
		# self.softmax = nn.Softmax(dim=output_dim)
		self.fc2 = nn.Linear(input_dim, output_dim)
		self.softmax = nn.Softmax(dim=1)

	def forward(self, x):
		x = self.fc2(x)
		x = self.softmax(x)
		return x
		# x shape: (batch_size, input_dim)
		# x = x.unsqueeze(1)  # (batch_size, 1, input_dim)
		# x = self.conv1(x)   # (batch_size, 16, input_dim)
		# x = self.relu(x)
		# x = self.pool(x)    # (batch_size, 16, input_dim//2)
		# x = self.dropout(x)
		# x = x.view(x.size(0), -1)  # flatten
		# x = self.fc1(x)
		# x = self.relu(x)
		# x = self.dropout(x)
		# x = self.fc2(x)
		# return x
