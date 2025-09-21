import time
import random
import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shap

from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (f1_score, precision_score, recall_score,
                             roc_auc_score, accuracy_score, confusion_matrix,
                             ConfusionMatrixDisplay, roc_curve, auc)
from lightgbm import LGBMClassifier

# -----------------------------
# Config & File Paths
# -----------------------------
idmap_train_path = "idmap.csv"
train_path = "disease_methylation_data.h5"
siteList = "disease_CpG_sites.txt"
annotation_file = "annotation_filtered.csv"
ewas_file = "EWAS_results.csv"

topN = 800  # number of top contributing features
disease = "Alzheimer's disease"
control = "control"
alpha = 3e-6  # significance threshold for Bonferroni

# -----------------------------
# Set Random Seed
# -----------------------------
seed = int(time.time())
np.random.seed(seed)
random.seed(seed)

# -----------------------------
# Load EWAS Results & Annotation
# -----------------------------
def load_ewas_results(ewas_path, annotation_path, cpg_sites_path):
    ewas_results = pd.read_csv(ewas_path)
    annotation = pd.read_csv(annotation_path)
    cpg_sites = pd.read_csv(cpg_sites_path, header=None)[0].tolist()

    # Map CpG index → IlmnID
    ewas_results["IlmnID"] = ewas_results["CpG_Index"].map(lambda idx: cpg_sites[idx])

    # Merge with annotation
    ewas_results = pd.merge(
        ewas_results,
        annotation[["IlmnID", "CHR", "MAPINFO"]],
        on="IlmnID",
        how="left"
    ).dropna(subset=["CHR", "MAPINFO"])

    # Calculate -log10 p-values
    ewas_results["-log10_p"] = -np.log10(ewas_results["p_value"].replace(0, np.nextafter(0,1)))

    # Bonferroni threshold
    n_tests = ewas_results.shape[0]
    line_height = -np.log10(alpha / n_tests)

    # Select significant CpGs
    significant_sites = ewas_results[ewas_results["-log10_p"] > line_height]
    featureIndices = [cpg_sites.index(cpg) for cpg in significant_sites["IlmnID"] if cpg in cpg_sites]

    print(f"Number of significant CpGs: {significant_sites.shape[0]}")
    return ewas_results, significant_sites, featureIndices, line_height

# -----------------------------
# Manhattan Plot
# -----------------------------
def plot_manhattan(df, threshold, filename="manhattan_plot.png"):
    df = df.sort_values(["CHR", "MAPINFO"])
    df["CHR"] = df["CHR"].astype(str)

    chr_sizes = df.groupby("CHR")["MAPINFO"].max().cumsum()
    chr_offsets = chr_sizes.shift(fill_value=0)
    df["BP_cum"] = df.apply(lambda row: row["MAPINFO"] + chr_offsets[row["CHR"]], axis=1)

    plt.figure(figsize=(14,6))
    colors = ["#1f77b4", "#ff7f0e"]
    for i, (chrom, group) in enumerate(df.groupby("CHR")):
        plt.scatter(group["BP_cum"], group["-log10_p"], 
                    c=colors[i % len(colors)], s=10, alpha=0.6)

    plt.axhline(y=threshold, color="red", linestyle="--")
    plt.xlabel("Genomic Position")
    plt.ylabel("-log10(p-value)")
    plt.title("Manhattan Plot of EWAS")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

# -----------------------------
# Volcano Plot
# -----------------------------
def plot_volcano(df, threshold, filename="volcano_plot.png"):
    plt.figure(figsize=(10,7))
    sns.scatterplot(data=df, x="t_stat", y="-log10_p", 
                    hue=df["-log10_p"] > threshold, 
                    palette={True:"red", False:"gray"},
                    alpha=0.7, edgecolor=None)

    plt.axhline(threshold, color="blue", linestyle="--", label="Bonferroni Threshold")
    plt.xlabel("t-statistic")
    plt.ylabel("-log10(p-value)")
    plt.title("Volcano Plot of EWAS")
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

# -----------------------------
# Load HDF5 methylation data
# -----------------------------
def load_methylation_data(h5_path, sample_indices, feature_indices):
    with h5py.File(h5_path, "r") as f:
        methylation = f["data"][sample_indices, :][:, feature_indices]
    return methylation

# -----------------------------
# Load ID mapping
# -----------------------------
def load_idmap(idmap_path, disease, control):
    idmap = pd.read_csv(idmap_path)
    mask = (idmap['disease_state'] == disease) | (idmap['disease_state'] == control)
    disease_selection = idmap[mask].copy()
    disease_selection['disease_state'] = disease_selection['disease_state'].replace({disease:1, control:0})
    disease_type = disease_selection.disease_state.to_numpy()
    selected_indices = idmap.index[mask].to_numpy()
    return disease_type, selected_indices

# -----------------------------
# Evaluation Function
# -----------------------------
def evaluate_model(y_true, y_pred, y_proba, topN):
    rocauc = roc_auc_score(y_true, y_proba)
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    pre = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)

    print(f"F1 Score: {f1:.3f}, Accuracy: {acc:.3f}, Precision: {pre:.3f}, Recall: {rec:.3f}, AUC: {rocauc:.3f}")

    # Save metrics
    try:
        evaluations = pd.read_csv('disease_evaluation_metrics.csv')
    except FileNotFoundError:
        evaluations = pd.DataFrame()

    results = pd.DataFrame([{
        "Feature Chunks": f"Top {topN}",
        "AUC": rocauc,
        "F1 Score": f1,
        "Accuracy": acc,
        "Precision": pre,
        "Recall": rec
    }])
    evaluations = pd.concat([evaluations, results], ignore_index=True)
    evaluations.to_csv('disease_evaluation_metrics.csv', index=False)

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    ConfusionMatrixDisplay(cm, display_labels=["Control", "Alzheimer's"]).plot()
    plt.title("Confusion Matrix")
    plt.savefig("confusion_matrix.png", dpi=300)
    plt.close()

    # ROC curve
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    plt.plot(fpr, tpr, label=f'AUC = {rocauc:.2f}')
    plt.plot([0,1],[0,1],'k--')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()
    plt.savefig("roc_curve.png", dpi=300)
    plt.close()

# -----------------------------
# Main
# -----------------------------
def main():
    # Load EWAS & select top features
    ewas_results, significant_sites, feature_indices, threshold = load_ewas_results(
        ewas_file,
        annotation_file,
        siteList
    )

    # Save Manhattan & Volcano plots
    plot_manhattan(ewas_results, threshold, "manhattan_plot.png")
    plot_volcano(ewas_results, threshold, "volcano_plot.png")

    # Load samples of interest
    disease_type, sample_indices = load_idmap(idmap_train_path, disease, control)
    methylation = load_methylation_data(train_path, sample_indices, feature_indices)

    print(f"Methylation matrix shape: {methylation.shape}")

    # Train LightGBM classifier
    params = {
        "boosting_type": "gbdt",
        "objective": "binary",
        "metric": "auc",
        "verbosity": 1,
        "is_unbalance": True,
        'learning_rate': 0.095,
        'num_leaves': 54,
        'max_depth': 4,
        'feature_fraction': 0.2,
        'bagging_fraction': 0.55,
        'bagging_freq': 3,
        'lambda_l1': 1.66,
        'lambda_l2': 3.36
    }
    model = LGBMClassifier(**params)
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

    print("Training model...")
    model.fit(methylation, disease_type)
    y_pred = cross_val_predict(model, methylation, disease_type, cv=cv)
    y_proba = cross_val_predict(model, methylation, disease_type, cv=cv, method="predict_proba")[:,1]

    # Evaluate
    evaluate_model(disease_type, y_pred, y_proba, topN)

    # SHAP Analysis
    print("Computing SHAP values...")
    explainer = shap.Explainer(model, methylation)
    shap_values = explainer(methylation)

    # Map CpG names
    with open(siteList, "r") as f:
        feature_names = np.array(f.read().splitlines())
    shap_values.feature_names = feature_names[feature_indices]

    shap.summary_plot(shap_values, methylation, show=False)
    plt.title("SHAP Summary Plot")
    plt.savefig("shap_summary.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    main()
