import requests
import json

def quick_test():
    print("🧬 Quick Backend Test")
    print("-" * 30)
    
    # Test demo prediction
    try:
        response = requests.post('http://localhost:8000/api/v1/predict-demo', timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Demo: {result['prediction']} ({result['risk_percentage']:.1f}% risk)")
            print(f"   Confidence: {result['confidence']*100:.1f}%")
            print(f"   Risk Level: {result['risk_level']}")
        else:
            print(f"❌ Demo failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Demo error: {e}")
    
    # Test health
    try:
        response = requests.get('http://localhost:8000/api/v1/health', timeout=3)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Server: {health['status']} (Model: {health['model_loaded']})")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health error: {e}")
    
    print("\n🌐 Web: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    quick_test()
