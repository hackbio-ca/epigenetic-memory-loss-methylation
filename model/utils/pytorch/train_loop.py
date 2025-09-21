import torch
import torch.nn as nn

def train_loop(dataloader, model, loss_fn, optimizer, batch_size):
    """
    Simplified training loop - shows metrics for the entire epoch
    
    Args:
        dataloader: Training data loader
        model: PyTorch model
        loss_fn: Loss function (typically nn.CrossEntropyLoss())
        optimizer: Optimizer (e.g., Adam, SGD)
        batch_size: Batch size for training
    
    Returns:
        model: Trained model
    """
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.train()  # Set model to training mode
    
    # Epoch-level metrics
    total_loss = 0.0
    correct_predictions = 0
    
    for batch, (X, y) in enumerate(dataloader):
        # Forward pass
        logits = model(X)
        
        # Compute cross-entropy loss (PyTorch built-in)
        loss = loss_fn(logits, y)
        
        # Backward pass and optimization
        optimizer.zero_grad()  # Clear gradients
        loss.backward()        # Compute gradients
        optimizer.step()       # Update parameters
        
        # Accumulate metrics for the epoch (computed consistently)
        with torch.no_grad():
            # Use the same logits for both loss and accuracy
            total_loss += loss.item()
            predictions = torch.argmax(logits, dim=1)
            correct_predictions += (predictions == y).sum().item()
    
    # Calculate epoch metrics
    avg_loss = total_loss / num_batches
    accuracy = (correct_predictions / size) * 100
    
    print(f"Training - Loss: {avg_loss:.6f}, Accuracy: {accuracy:.2f}%")
    
    return model