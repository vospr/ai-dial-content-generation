"""
Automatic Test Script for DIAL API Image Generation and Analysis
Runs all tests without pauses for verification
"""
import sys
import os

# Add task directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'task'))

def run_test(test_name, test_function):
    """Run a test with error handling"""
    print("\n" + "="*70)
    print(f"🚀 Starting: {test_name}")
    print("="*70 + "\n")
    
    try:
        test_function()
        print(f"\n✅ {test_name} completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ {test_name} failed with error:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*70)
    print("DIAL API IMAGE GENERATION AND ANALYSIS - AUTOMATED TESTS")
    print("="*70 + "\n")
    
    results = []
    
    # Test 1: OpenAI-style Image Analysis (Base64 encoding)
    def test_openai_itt():
        from task.image_to_text.openai.task_openai_itt import start
        start()
    
    results.append(("Test 1: OpenAI-Style Image Analysis", 
                   run_test("Test 1: OpenAI-Style Image Analysis (Base64)", test_openai_itt)))
    
    # Test 2: DIAL-style Image Analysis (Bucket storage)
    def test_dial_itt():
        from task.image_to_text.task_dial_itt import start
        start()
    
    results.append(("Test 2: DIAL-Style Image Analysis", 
                   run_test("Test 2: DIAL-Style Image Analysis (Bucket Storage)", test_dial_itt)))
    
    # Test 3: Text-to-Image Generation
    def test_tti():
        from task.text_to_image.task_tti import start
        start()
    
    results.append(("Test 3: Text-to-Image Generation", 
                   run_test("Test 3: Text-to-Image Generation", test_tti)))
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {status}: {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print("\n" + "="*70)
    print(f"Results: {passed_count}/{total_count} tests passed")
    print("="*70 + "\n")
    
    return all(passed for _, passed in results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

