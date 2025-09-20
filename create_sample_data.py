import pandas as pd
import numpy as np

def create_sample_methylation_data():
    np.random.seed(42)
    
    # Create 500 CpG sites (features)
    cpg_sites = [f"cg{i:06d}" for i in range(500)]
    
    # Create 3 sample patients with realistic methylation values
    samples = {
        'CpG Sites': cpg_sites,
        'Patient_1': np.random.beta(2, 2, 500),  # Control-like
        'Patient_2': np.random.beta(3, 2, 500),  # MCI-like  
        'Patient_3': np.random.beta(2, 3, 500)   # Alzheimer's-like
    }
    
    df = pd.DataFrame(samples)
    
    # Save to CSV
    df.to_csv('sample_methylation_data_500.csv', index=False)
    print("✅ Created sample_methylation_data_500.csv with 500 features")
    print(f"   Shape: {df.shape}")
    print(f"   Features: {len(cpg_sites)} CpG sites")
    print(f"   Samples: 3 patients")
    print(f"   Data range: {df.iloc[:, 1:].min().min():.3f} - {df.iloc[:, 1:].max().max():.3f}")

if __name__ == "__main__":
    create_sample_methylation_data()

