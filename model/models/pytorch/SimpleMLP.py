# Alternative Fully Connected Model for Methylation Data
import torch
import torch.nn as nn

class SimpleMLP(nn.Module):
    """
    Simple Multi-Layer Perceptron for tabular methylation data
    Often more appropriate than CNN for this type of data
    """
    def __init__(self, input_dim, hidden_dims=[512, 128, 128, 32], output_dim=3, dropout_rate=0.3):
        super(SimpleMLP, self).__init__()
        
        layers = []
        prev_dim = input_dim
        
        # Build hidden layers
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.BatchNorm1d(hidden_dim),
                nn.Dropout(dropout_rate)
            ])
            prev_dim = hidden_dim
        
        # Output layer
        layers.append(nn.Linear(prev_dim, output_dim))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)