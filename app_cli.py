import requests
import json
import time
from typing import Dict, Any

class MethylationCLI:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    def check_server(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/v1/health", timeout=5)
            if response.status_code == 200:
                health = response.json()
                print(f"✅ Server Status: {health['status']}")
                print(f"✅ Model Loaded: {health['model_loaded']}")
                return True
            else:
                print(f"❌ Server Error: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to server. Make sure it's running on localhost:8000")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def test_demo_prediction(self) -> Dict[str, Any]:
        try:
            print("\n🧬 Testing Demo Prediction...")
            response = requests.post(f"{self.base_url}/api/v1/predict-demo", timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Demo Prediction Successful!")
                return result
            else:
                print(f"❌ Demo Prediction Failed: {response.status_code}")
                print(f"Error: {response.text}")
                return {}
        except Exception as e:
            print(f"❌ Demo Prediction Error: {e}")
            return {}
    
    def display_results(self, result: Dict[str, Any]):
        if not result:
            return
            
        print("\n" + "="*60)
        print("📊 PREDICTION RESULTS")
        print("="*60)
        
        # Main prediction
        prediction = result.get('prediction', 'Unknown')
        confidence = result.get('confidence', 0) * 100
        risk_level = result.get('risk_level', 'Unknown')
        risk_percentage = result.get('risk_percentage', 0)
        
        print(f"🎯 Prediction: {prediction}")
        print(f"📈 Confidence: {confidence:.1f}%")
        print(f"⚠️  Risk Level: {risk_level}")
        print(f"📊 Risk Percentage: {risk_percentage:.1f}%")
        
        # Probabilities
        probabilities = result.get('probabilities', {})
        if probabilities:
            print(f"\n📋 Class Probabilities:")
            for class_name, prob in probabilities.items():
                print(f"   {class_name}: {prob*100:.1f}%")
        
        # Model insights
        model_insights = result.get('model_insights', {})
        if model_insights:
            print(f"\n🔬 Model Information:")
            print(f"   Model Type: {model_insights.get('model_type', 'Unknown')}")
            print(f"   Features Analyzed: {model_insights.get('total_features', 'Unknown')}")
            if model_insights.get('model_accuracy'):
                print(f"   Model Accuracy: {model_insights['model_accuracy']*100:.1f}%")
        
        # Calibration
        calibration = result.get('calibration_score')
        if calibration:
            print(f"   Model Reliability: {calibration*100:.1f}%")
        
        print("="*60)
    
    def test_file_upload(self, file_path: str = "out.csv"):
        try:
            print(f"\n📁 Testing File Upload: {file_path}")
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{self.base_url}/api/v1/predict", files=files, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ File Upload Successful!")
                return result
            else:
                print(f"❌ File Upload Failed: {response.status_code}")
                print(f"Error: {response.text}")
                return {}
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
            return {}
        except Exception as e:
            print(f"❌ File Upload Error: {e}")
            return {}
    
    def get_model_info(self):
        try:
            print("\n🔍 Getting Model Information...")
            response = requests.get(f"{self.base_url}/api/v1/model-info", timeout=5)
            
            if response.status_code == 200:
                info = response.json()
                print("✅ Model Info Retrieved!")
                print(f"   Model Type: {info.get('model_type', 'Unknown')}")
                print(f"   Model Loaded: {info.get('model_loaded', False)}")
                print(f"   Total Features: {info.get('total_features', 'Unknown')}")
                print(f"   Model Accuracy: {info.get('model_accuracy', 'Unknown')}")
                return info
            else:
                print(f"❌ Model Info Failed: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ Model Info Error: {e}")
            return {}
    
    def run_full_test(self):
        print("🧬 Epigenetic Memory Loss Methylation - CLI Test")
        print("="*60)
        
        # Check server
        if not self.check_server():
            return
        
        # Get model info
        self.get_model_info()
        
        # Test demo prediction
        demo_result = self.test_demo_prediction()
        if demo_result:
            self.display_results(demo_result)
        
        # Test file upload if sample file exists
        try:
            with open("out.csv", 'r'):
                file_result = self.test_file_upload()
                if file_result:
                    print("\n📁 File Upload Results:")
                    self.display_results(file_result)
        except FileNotFoundError:
            print("\n📁 out.csv file not found, skipping file upload test")
        
        print("\n🎉 All tests completed!")
        print("🌐 Web interface available at: http://localhost:8000")
        print("📚 API docs available at: http://localhost:8000/docs")

def main():
    cli = MethylationCLI()
    cli.run_full_test()

if __name__ == "__main__":
    main()
