import torch
import torch.nn as nn
from torch import argmax
from torch.nn.functional import softmax
import numpy as np
from sklearn.metrics import precision_recall_fscore_support, classification_report, confusion_matrix

def test_loop(dataloader, model, loss_fn, num_classes=3, class_names=None):
    """
    Enhanced test loop for 3-class categorical classification
    
    Args:
        dataloader: Test data loader
        model: Trained model
        loss_fn: Loss function (CrossEntropyLoss)
        num_classes: Number of classes (default: 3)
        class_names: List of class names for reporting (optional)
    
    Returns:
        dict: Dictionary containing all metrics
    """
    # Set default class names if not provided
    if class_names is None:
        class_names = [f'Class_{i}' for i in range(num_classes)]
    
    # Set the model to evaluation mode
    model.eval()
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    
    # Initialize metrics
    total_loss = 0.0
    correct_predictions = 0
    
    # Collect all predictions and targets for detailed metrics
    all_predictions = []
    all_targets = []
    all_probabilities = []

    # Evaluating the model with torch.no_grad() ensures that no gradients are computed during test mode
    with torch.no_grad():
        for X, y in dataloader:
            # Forward pass
            logits = model(X)
            
            # Compute cross-entropy loss
            batch_loss = loss_fn(logits, y)
            total_loss += batch_loss.item()
            
            # Get predictions and probabilities
            probabilities = torch.softmax(logits, dim=1)
            predictions = torch.argmax(logits, dim=1)
            
            # Count correct predictions
            correct_predictions += (predictions == y).sum().item()
            
            # Store for detailed metrics computation (convert to Python lists directly)
            all_predictions.extend(predictions.tolist())
            all_targets.extend(y.tolist())
            all_probabilities.extend(probabilities.tolist())
    
    # Convert to numpy arrays for sklearn metrics
    all_predictions = np.array(all_predictions)
    all_targets = np.array(all_targets)
    # Keep probabilities as list of lists for now
    
    # Compute primary metrics
    avg_loss = total_loss / num_batches  # Average cross-entropy loss
    accuracy = correct_predictions / size  # Overall accuracy
    
    # Compute precision, recall, and F1-score for each class and overall
    precision, recall, f1, support = precision_recall_fscore_support(
        all_targets, all_predictions, 
        labels=list(range(num_classes)), 
        average=None, 
        zero_division=0
    )
    
    # Compute macro and weighted averages
    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
        all_targets, all_predictions, average='macro', zero_division=0
    )
    
    precision_weighted, recall_weighted, f1_weighted, _ = precision_recall_fscore_support(
        all_targets, all_predictions, average='weighted', zero_division=0
    )
    
    # Compute confusion matrix
    conf_matrix = confusion_matrix(all_targets, all_predictions, labels=list(range(num_classes)))
    
    # Print detailed results
    print(f"Test Results Summary:")
    print(f"{'='*60}")
    print(f"Overall Accuracy: {accuracy*100:.2f}%")
    print(f"Cross-Entropy Loss: {avg_loss:.6f}")
    print(f"{'='*60}")
    
    print(f"\nPer-Class Metrics:")
    print(f"{'Class':<15} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
    print(f"{'-'*65}")
    
    for i in range(num_classes):
        print(f"{class_names[i]:<15} {precision[i]:<12.3f} {recall[i]:<12.3f} {f1[i]:<12.3f} {support[i]:<10}")
    
    print(f"{'-'*65}")
    print(f"{'Macro Avg':<15} {precision_macro:<12.3f} {recall_macro:<12.3f} {f1_macro:<12.3f} {size:<10}")
    print(f"{'Weighted Avg':<15} {precision_weighted:<12.3f} {recall_weighted:<12.3f} {f1_weighted:<12.3f} {size:<10}")
    
    print(f"\nConfusion Matrix:")
    print(f"{'Predicted →':<12}", end="")
    for name in class_names:
        print(f"{name:<12}", end="")
    print()
    
    for i, name in enumerate(class_names):
        print(f"{'True ' + name:<12}", end="")
        for j in range(num_classes):
            print(f"{conf_matrix[i,j]:<12}", end="")
        print()
    
    print(f"{'='*60}")
    
    # Return comprehensive metrics dictionary
    metrics = {
        'accuracy': accuracy,
        'cross_entropy_loss': avg_loss,
        'precision_per_class': precision.tolist(),
        'recall_per_class': recall.tolist(),
        'f1_per_class': f1.tolist(),
        'support_per_class': support.tolist(),
        'precision_macro': precision_macro,
        'recall_macro': recall_macro,
        'f1_macro': f1_macro,
        'precision_weighted': precision_weighted,
        'recall_weighted': recall_weighted,
        'f1_weighted': f1_weighted,
        'confusion_matrix': conf_matrix.tolist(),
        'predictions': all_predictions.tolist(),
        'targets': all_targets.tolist(),
        'probabilities': all_probabilities,  # Already a list
        'class_names': class_names
    }
    
    return metrics