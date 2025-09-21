import numpy as np
import pandas as pd
import h5py
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests
from tqdm import tqdm   # progress bar

# === Load sample info ===
def load_idmap(idmap_dir, disease, control):
    idmap = pd.read_csv(idmap_dir)
    mask = (idmap['disease_state'] == disease) | (idmap['disease_state'] == control)
    diseaseSelection = idmap[mask].copy()
    diseaseSelection['disease_state'] = diseaseSelection['disease_state'].replace({disease: 1, control: 0})
    disease_type = diseaseSelection['disease_state'].to_numpy()
    sample_indices = idmap.index[mask].to_numpy()
    return disease_type, sample_indices

# === Load methylation data ===
def load_methylation_h5(path, sample_indices):
    with h5py.File(path, "r") as f:
        data = f["data"][sample_indices, :]  # samples × CpGs
    return data

# === EWAS function with progress tracking ===
def run_ewas(methylation, disease_type):
    n_features = methylation.shape[1]
    pvals = np.zeros(n_features)
    tvals = np.zeros(n_features)

    group1 = methylation[disease_type == 1]
    group0 = methylation[disease_type == 0]

    for i in tqdm(range(n_features), desc="Running EWAS"):
        try:
            t, p = mannwhitneyu(group1[:, i], group0[:, i], alternative='two-sided')
            pvals[i] = p
            tvals[i] = t
        except Exception:
            pvals[i] = np.nan
            tvals[i] = np.nan

    # Multiple testing correction
    reject, qvals, _, _ = multipletests(pvals, alpha=0.05, method="fdr_bh")

    results = pd.DataFrame({
        "CpG_Index": np.arange(n_features),
        "t_stat": tvals,
        "p_value": pvals,
        "q_value": qvals,
        "significant": reject
    })
    return results

# === Example usage ===
idmap_path = "idmap.csv"
h5_path = "disease_methylation_data.h5"
disease = "Alzheimer's disease"
control = "control"

disease_type, sample_indices = load_idmap(idmap_path, disease, control)
methylation = load_methylation_h5(h5_path, sample_indices)

print("Methylation shape:", methylation.shape)

# Run EWAS
ewas_results = run_ewas(methylation, disease_type)

# Save results
ewas_results.to_csv("EWAS_results.csv", index=False)
print("EWAS complete! Results saved to EWAS_results.csv")
print(ewas_results.head())
