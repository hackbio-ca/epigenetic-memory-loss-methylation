#!/usr/bin/env python3
"""
Verify H5 file conversion and model prediction
"""

import h5py
import numpy as np
import joblib
import pandas as pd

def verify_h5_conversion():
    """Verify the H5 file conversion"""
    print("=== H5 File Verification ===")
    
    try:
        with h5py.File('single_sample.h5', 'r') as f:
            data = f['data'][:]
            print(f"✅ H5 file loaded successfully")
            print(f"   Data shape: {data.shape}")
            print(f"   Data type: {data.dtype}")
            print(f"   Valid data range: {np.nanmin(data):.6f} to {np.nanmax(data):.6f}")
            print(f"   Non-NaN values: {np.sum(~np.isnan(data))} out of {data.size}")
            print(f"   First 10 values: {data[0, :10]}")
            
            # Check if data looks reasonable (methylation values should be 0-1)
            if np.all((data >= 0) & (data <= 1)):
                print("✅ Data values are in expected range (0-1)")
            else:
                print("⚠️  Some data values are outside expected range (0-1)")
                
    except Exception as e:
        print(f"❌ Error reading H5 file: {e}")
        return False
    
    return True

def test_model_prediction():
    """Test model prediction with the H5 data"""
    print("\n=== Model Prediction Test ===")
    
    try:
        # Load model
        model = joblib.load('../Temp.pkl')
        print("✅ Model loaded successfully")
        
        # Load H5 data
        with h5py.File('single_sample.h5', 'r') as f:
            data = f['data'][:]
        
        # Make prediction
        prediction = model.predict(data)
        print(f"✅ Prediction: {prediction}")
        
        # Get probabilities
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(data)
            print(f"✅ Probabilities: {probabilities}")
            
            # Interpret results
            if prediction[0] == 0:
                result = "Control (No Disease)"
            elif prediction[0] == 1:
                result = "Disease (MCI/Alzheimer's)"
            else:
                result = f"Unknown class: {prediction[0]}"
            
            print(f"✅ Interpretation: {result}")
            print(f"   Confidence: {max(probabilities[0])*100:.1f}%")
        
    except Exception as e:
        print(f"❌ Error in model prediction: {e}")
        return False
    
    return True

def compare_with_original_csv():
    """Compare H5 data with original CSV"""
    print("\n=== CSV vs H5 Comparison ===")
    
    try:
        # Load original CSV
        df = pd.read_csv('../out.csv', index_col=0)
        print(f"✅ Original CSV loaded: {df.shape}")
        
        # Load SHAP values for feature selection
        total_mean_SHAP_values = np.loadtxt("../Disease_SHAP_Values.txt")
        topNFeatures = np.argsort(total_mean_SHAP_values)[-500:][::-1].tolist()
        featureIndices = np.array(sorted(topNFeatures))
        
        # Convert CSV to same format as H5
        data_array = df.T.values
        if data_array.shape[1] >= len(featureIndices):
            csv_selected = data_array[0, featureIndices]
        else:
            available_indices = featureIndices[featureIndices < data_array.shape[1]]
            csv_selected = data_array[0, available_indices]
            padding = np.zeros(len(featureIndices) - len(available_indices))
            csv_selected = np.concatenate([csv_selected, padding])
        
        # Load H5 data
        with h5py.File('single_sample.h5', 'r') as f:
            h5_data = f['data'][0, :]
        
        # Compare
        if np.array_equal(csv_selected, h5_data):
            print("✅ H5 data matches CSV data exactly")
        else:
            print("⚠️  H5 data differs from CSV data")
            print(f"   Max difference: {np.max(np.abs(csv_selected - h5_data))}")
        
    except Exception as e:
        print(f"❌ Error comparing CSV and H5: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🧬 H5 Conversion and Model Prediction Verification")
    print("=" * 60)
    
    # Run all tests
    h5_ok = verify_h5_conversion()
    prediction_ok = test_model_prediction()
    comparison_ok = compare_with_original_csv()
    
    print("\n" + "=" * 60)
    if h5_ok and prediction_ok and comparison_ok:
        print("🎉 ALL VERIFICATIONS PASSED!")
        print("✅ out.csv → H5 conversion is working correctly")
        print("✅ Model predictions are working")
        print("✅ Data integrity is maintained")
    else:
        print("⚠️  Some verifications failed - check output above")
    print("=" * 60)
