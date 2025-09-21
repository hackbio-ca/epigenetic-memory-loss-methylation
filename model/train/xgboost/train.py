from model.models.xgboost.model import XGBoostModel
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score

import pandas as pd
import numpy as np
import time, os, argparse

import sys
sys.path.append('./model')

from data.loaders.loader_xgboost import load_data, load_data_h5

def kfold_cv(model, X, y, k=5):
    """
    Perform K-Fold Cross Validation
    """
    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    precision_list, recall_list, accuracy_list, f1_list = [], [], [], []

    for train_index, val_index in kf.split(X):
        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y[train_index], y[val_index]

        model.train(X_train, y_train)
        y_pred = model.predict(X_val)

        precision_list.append(precision_score(y_val, y_pred, average='weighted'))
        recall_list.append(recall_score(y_val, y_pred, average='weighted'))
        accuracy_list.append(accuracy_score(y_val, y_pred))
        f1_list.append(f1_score(y_val, y_pred, average='weighted'))
    
    return precision_list, recall_list, accuracy_list, f1_list



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train XGBoost model with optional grid search.")
    parser.add_argument('--grid-search', action='store_true', help='Run grid search for hyperparameters')
    args = parser.parse_args()

    # Train Options (Settings)
    params = {
        "max_depth": 13,
        "learning_rate": 0.1,
        "n_estimators": 100,
        "objective": "recall_weighted",
        "booster": "gbtree",
        "gamma": 0,
        "min_child_weight": 1,
        "subsample": 1,
        "colsample_bytree": 1,
        "reg_alpha": 0,
        "reg_lambda": 1,
        "random_state": int(time.time()),
    }

    # Train data
    data_train_path = './model/data/train/methylation.csv'
    data_train_h5 = './model/data/train/methylation.h5'
    idmap_train_path = './model/data/train/idmap.csv'
    # Test data
    data_test_path = './model/data/test/methylation.csv'
    idmap_test_path = './model/data/test/idmap.csv'

    # Load Train Data
    # X_train, y_train = load_data(data_train_path, idmap_train_path)
    X_train, y_train = load_data_h5(data_train_h5, idmap_train_path)
    print(f"Train data shape: {X_train.shape}, Train label shape: {y_train.shape}")

    model = XGBoostModel(params=params)

    if args.grid_search:
        # Run Search for Best Model HPs
        search_params = {
            # "max_depth": [3,5,7,10],
            # "n_estimators": [50, 100, 200],
            # "learning_rate": [0.01, 0.1, 0.3],
            # "reg_alpha": [0, 0.01, 0.05, 0.1],
            # "reg_lambda": [0, 0.01, 0.05, 0.1],
            "classifier__solver": ['liblinear', 'lbfgs'],
            "classifier__C": [0.1, 1, 10]
        }
        best_model = model.search_cv(search_params, X_train, y_train)
        best_model.train(X_train, y_train)
        # Save Model
        save_path = './model/models/xgboost/'
        os.makedirs(save_path, exist_ok=True)
        best_model.save_model(save_path)
    else:
        # Standard training
        precision_list, recall_list, accuracy_list, f1_list = kfold_cv(model, X_train, y_train)
        # Print results
        print(f"K-Fold CV Results (k=5):")
        print(f"Precision: {np.mean(precision_list):.4f} ± {np.std(precision_list):.4f}")
        print(f"Recall: {np.mean(recall_list):.4f} ± {np.std(recall_list):.4f}")
        print(f"Accuracy: {np.mean(accuracy_list):.4f} ± {np.std(accuracy_list):.4f}")
        print(f"F1 Score: {np.mean(f1_list):.4f} ± {np.std(f1_list):.4f}")
        # Save Model
        save_path = './model/models/xgboost/'
        os.makedirs(save_path, exist_ok=True)
        model.save_model(save_path)