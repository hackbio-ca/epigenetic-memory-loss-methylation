"""
Test script to validate the backend setup and API functionality.
"""
import sys
import json
import asyncio
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.config import get_settings
from app.services import get_model_service
from app.controllers import prediction_controller
from app.models.schemas import PredictionRequest, ModelType


async def test_configuration():
    """Test configuration loading."""
    print("🔧 Testing configuration...")
    settings = get_settings()
    print(f"✅ App name: {settings.app_name}")
    print(f"✅ Version: {settings.app_version}")
    print(f"✅ XGBoost model path: {settings.xgboost_model_path}")
    print(f"✅ PyTorch model path: {settings.pytorch_model_path}")
    return True


async def test_model_service():
    """Test model service functionality."""
    print("\n🤖 Testing model service...")
    
    model_service = get_model_service()
    loaded_models = model_service.get_loaded_models()
    
    print(f"📊 Model loading status:")
    for model_name, is_loaded in loaded_models.items():
        status = "✅" if is_loaded else "❌"
        print(f"  {status} {model_name}: {'Loaded' if is_loaded else 'Failed to load'}")
    
    if any(loaded_models.values()):
        print("✅ At least one model is loaded successfully")
        return True
    else:
        print("❌ No models are loaded")
        return False


async def test_prediction():
    """Test prediction functionality."""
    print("\n🎯 Testing predictions...")
    
    # Sample data for testing
    test_data = [
        [1.0, 2.0, 3.0, 4.0, 5.0],
        [2.0, 3.0, 4.0, 5.0, 6.0]
    ]
    
    try:
        # Test with both models
        request = PredictionRequest(
            data=test_data,
            model_type=ModelType.BOTH
        )
        
        response = await prediction_controller.predict(request)
        
        print(f"✅ Prediction successful: {response.success}")
        print(f"✅ Message: {response.message}")
        print(f"✅ Number of results: {len(response.results)}")
        
        for result in response.results:
            print(f"  📈 {result.model_name}: {len(result.prediction)} predictions")
            if result.confidence:
                print(f"    🎯 Confidence: {result.confidence:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return False


async def test_individual_models():
    """Test individual model predictions."""
    print("\n🔍 Testing individual models...")
    
    test_data = [[1.0, 2.0, 3.0, 4.0, 5.0]]
    
    for model_type in [ModelType.XGBOOST, ModelType.PYTORCH]:
        try:
            request = PredictionRequest(
                data=test_data,
                model_type=model_type
            )
            
            response = await prediction_controller.predict(request)
            print(f"✅ {model_type.value} model: Success")
            
        except Exception as e:
            print(f"❌ {model_type.value} model: {e}")


async def main():
    """Run all tests."""
    print("🧪 Backend API Test Suite")
    print("=" * 50)
    
    tests = [
        test_configuration,
        test_model_service,
        test_prediction,
        test_individual_models
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary")
    passed = sum(1 for r in results if r is True)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All tests passed! ({passed}/{total})")
        print("✅ Backend is ready to run!")
    else:
        print(f"⚠️  Some tests failed: {passed}/{total} passed")
        print("🔧 Please check the configuration and model files")
    
    print("\n🚀 To start the server, run:")
    print("   python main.py")
    print("   OR")
    print("   ./start.sh (Linux/macOS)")
    print("   start.bat (Windows)")


if __name__ == "__main__":
    asyncio.run(main())