import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
ewas_results = pd.read_csv("EWAS_results.csv")

def plot_volcano(ewas_results, top_n=20):
    # Avoid log(0) errors
    ewas_results = ewas_results.copy()
    ewas_results["-log10_p"] = -np.log10(ewas_results["p_value"].replace(0, np.nextafter(0, 1)))

    plt.figure(figsize=(10, 7))
    sns.scatterplot(
        data=ewas_results,
        x="t_stat", 
        y="-log10_p",
        hue="significant",
        palette={True: "red", False: "gray"},
        alpha=0.7,
        edgecolor=None
    )

    plt.axhline(-np.log10(0.05), color="blue", linestyle="--", label="p=0.05")

    plt.xlabel("t-statistic (effect size)")
    plt.ylabel("-log10(p-value)")
    plt.title("Volcano Plot of EWAS Results")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_manhattan(ewas_results, significance=0.05):
    # Make sure we don’t take log of 0
    ewas_results = ewas_results.copy()
    ewas_results["-log10_p"] = -np.log10(ewas_results["p_value"].replace(0, np.nextafter(0, 1)))

    # Sort by chromosome and position
    ewas_results = ewas_results.sort_values(["CHR", "MAPINFO"])
    
    # Compute cumulative base pair positions
    ewas_results["CHR"] = ewas_results["CHR"].astype(str)
    chr_sizes = ewas_results.groupby("CHR")["MAPINFO"].max().cumsum()
    chr_offsets = chr_sizes.shift(fill_value=0)
    ewas_results["BP_cum"] = ewas_results.apply(lambda row: row["MAPINFO"] + chr_offsets[row["CHR"]], axis=1)

    # Plot
    plt.figure(figsize=(14, 6))
    colors = ["#1f77b4", "#ff7f0e"]  # alternating colors per chromosome
    for i, (chrom, group) in enumerate(ewas_results.groupby("CHR")):
        plt.scatter(
            group["BP_cum"], group["-log10_p"],
            c=colors[i % len(colors)], s=10, alpha=0.6, label=f"Chr {chrom}"
        )

    alpha = 0.00005
    threshold = alpha / ewas_results.shape[0]   # Bonferroni
    print(threshold)
    print(ewas_results.shape[0])
    line_height = -np.log10(threshold)
    print(line_height)

    plt.axhline(y=line_height, color="red", linestyle="--")

    plt.xlabel("Genomic Position")
    plt.ylabel("-log10(p-value)")
    plt.title("Manhattan Plot of EWAS")
    plt.legend(markerscale=2, fontsize=8)
    plt.tight_layout()
    plt.show()

# Example usage after running EWAS:
#plot_volcano(ewas_results)

# Load annotation file (Illumina manifest)
annotation = pd.read_csv("annotation_filtered.csv")  
# This file should already have the columns: IlmnID, CHR, MAPINFO, etc.

# Load CpG site list (in the same order as your HDF5 file columns)
cpg_sites = pd.read_csv("disease_CpG_sites.txt", header=None)[0].tolist()

# After EWAS, your results likely have indices
# e.g., "CpG" column contains feature indices

# Map index → CpG ID
ewas_results["IlmnID"] = ewas_results["CpG_Index"].map(lambda idx: cpg_sites[idx])
# Now merge with annotation on IlmnID
ewas_results = pd.merge(
    ewas_results,
    annotation[["IlmnID", "CHR", "MAPINFO"]],
    on="IlmnID",
    how="left"
)

# Drop any sites that didn’t get annotation (optional)
ewas_results = ewas_results.dropna(subset=["CHR", "MAPINFO"])

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 1) shapes & group counts
#print("methylation.shape:", methylation.shape)
#print("label counts:", np.unique(disease_type, return_counts=True))

# 2) p-value histogram and -log10 histogram
pvals = ewas_results["p_value"].values
pvals = pvals[np.isfinite(pvals) & (pvals>0)]
plt.figure(); plt.hist(pvals, bins=100); plt.title("p-value histogram"); plt.show()
plt.figure(); plt.hist(-np.log10(pvals), bins=100); plt.title("-log10 p histogram"); plt.show()

# 3) QQ-plot and lambda GC
obs = -np.log10(np.sort(pvals))
exp = -np.log10(np.linspace(1/len(pvals), 1, len(pvals)))
plt.figure(); plt.scatter(exp, obs, s=4); plt.plot([exp.min(),exp.max()],[exp.min(),exp.max()], 'r--'); plt.xlabel("Expected"); plt.ylabel("Observed"); plt.show()

chisq = stats.chi2.isf(pvals, 1)
lambda_gc = np.median(chisq) / stats.chi2.ppf(0.5, 1)
print("lambda GC:", lambda_gc)


plot_manhattan(ewas_results)