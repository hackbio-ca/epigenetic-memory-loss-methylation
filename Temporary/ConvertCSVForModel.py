import joblib
import pandas as pd
import numpy as np
import h5py
import io

#Load the pre-trained model
model = joblib.load('temp.pkl')

#Temporary
#Load selected features
total_mean_SHAP_values = np.loadtxt("Disease_SHAP_Values.txt")
topNFeatures = np.argsort(total_mean_SHAP_values)[-500:][::-1].tolist()
featureIndices = np.array(sorted(topNFeatures))
'''
with h5py.File("disease_methylation_data.h5", "r") as f:
    data = f["data"][0, ]   # shape: (n_samples, n_features)
    data = data.reshape(1, -1)

# Load feature list
Site_Names = pd.read_csv("disease_CpG_sites.txt", header=None, names=["CpG_Site"])
print(Site_Names)
Site_Names = Site_Names["CpG_Site"].tolist()

df = pd.DataFrame(data, columns=Site_Names).T
df.to_csv("out.csv", index=True)'''

# Load your CSV (out.csv created before)
df = pd.read_csv("out.csv", index_col=0)  # CpG sites are in the index
print(df.head())

# Convert back to numpy array
data_array = df.T.values   # shape will be (1, n_features)

# Create an HDF5 file and store it
with h5py.File("single_sample.h5", "w") as f:
    f.create_dataset("data", data=data_array)
    data = f["data"][0, featureIndices]
    data = data.reshape(1, -1)

prediction = model.predict(data)
print(prediction)