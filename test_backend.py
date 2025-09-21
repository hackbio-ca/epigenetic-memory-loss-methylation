import requests
import pandas as pd
import numpy as np
import time
import json

def test_backend():
    base_url = "http://localhost:8000"
    
    print("🧬 Testing Epigenetic Memory Loss Methylation Backend API...")
    print("=" * 60)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/health")
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {health_data['status']}")
            print(f"   Model loaded: {health_data['model_loaded']}")
            print(f"   Version: {health_data['version']}")
        else:
            print("❌ Health check failed")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running on localhost:8000")
        return
    
    # Test model info endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/model-info")
        if response.status_code == 200:
            model_info = response.json()
            print("✅ Model info retrieved")
            print(f"   Model loaded: {model_info['model_loaded']}")
            print(f"   Model type: {model_info['model_type']}")
            print(f"   Model accuracy: {model_info.get('model_accuracy', 'N/A')}")
        else:
            print("❌ Model info failed")
    except Exception as e:
        print(f"❌ Model info error: {e}")
    
    # Test demo data prediction
    try:
        response = requests.post(f"{base_url}/api/v1/predict-demo")
        if response.status_code == 200:
            result = response.json()
            print("✅ Demo prediction successful")
            print(f"   Sample ID: {result['sample_id']}")
            print(f"   Prediction: {result['prediction']}")
            print(f"   Confidence: {result['confidence']:.2%}")
            print(f"   Risk Level: {result['risk_level']}")
            print(f"   Risk Percentage: {result['risk_percentage']:.1f}%")
            print(f"   Calibration Score: {result.get('calibration_score', 'N/A')}")
            print("   Probabilities:")
            for class_name, prob in result['probabilities'].items():
                print(f"     {class_name}: {prob:.2%}")
        else:
            print(f"❌ Demo prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Demo prediction error: {e}")
    
    # Test file upload prediction
    try:
        with open('sample_methylation_data.csv', 'rb') as f:
            response = requests.post(f"{base_url}/api/v1/predict", files={'file': f})
            if response.status_code == 200:
                result = response.json()
                print("✅ File upload prediction successful")
                print(f"   Sample ID: {result['sample_id']}")
                print(f"   Prediction: {result['prediction']}")
                print(f"   Confidence: {result['confidence']:.2%}")
                print(f"   Risk Level: {result['risk_level']}")
                print(f"   Risk Percentage: {result['risk_percentage']:.1f}%")
            else:
                print(f"❌ File upload prediction failed: {response.status_code}")
                print(f"   Error: {response.text}")
    except FileNotFoundError:
        print("❌ Sample data file not found. Please ensure sample_methylation_data.csv exists")
    except Exception as e:
        print(f"❌ File upload prediction error: {e}")
    
    # Test JSON prediction endpoint
    try:
        sample_data = np.random.rand(1, 500).tolist()
        payload = {
            "methylation_data": sample_data,
            "sample_id": "test_sample"
        }
        
        response = requests.post(f"{base_url}/api/v1/predict-json", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ JSON prediction successful")
            print(f"   Sample ID: {result['sample_id']}")
            print(f"   Prediction: {result['prediction']}")
            print(f"   Confidence: {result['confidence']:.2%}")
            print(f"   Risk Level: {result['risk_level']}")
        else:
            print(f"❌ JSON prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ JSON prediction error: {e}")
    
    # Test sample data info endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/sample-data-info")
        if response.status_code == 200:
            sample_info = response.json()
            print("✅ Sample data info retrieved")
            print(f"   Description: {sample_info['description']}")
            print(f"   Features: {sample_info['features']}")
            print(f"   Samples: {sample_info['samples']}")
        else:
            print("❌ Sample data info failed")
    except Exception as e:
        print(f"❌ Sample data info error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Backend API Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    print("Waiting 3 seconds for server to be ready...")
    time.sleep(3)
    test_backend()

