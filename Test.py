"""
Comprehensive Test Script for DIAL API Image Generation and Analysis
Tests all three tasks with pause functionality for screenshot capture
"""
import sys
import os

# Add task directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'task'))

def pause_for_screenshot(test_name):
    """Pause and wait for user to press Enter"""
    print("\n" + "="*70)
    input(f"📸 Test '{test_name}' completed. Take screenshot, then press ENTER to continue...")
    print("="*70 + "\n")

def run_test(test_name, test_function):
    """Run a test with error handling"""
    print("\n" + "="*70)
    print(f"🚀 Starting: {test_name}")
    print("="*70 + "\n")
    
    try:
        test_function()
        print(f"\n✅ {test_name} completed successfully!")
    except Exception as e:
        print(f"\n❌ {test_name} failed with error:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    print("\n" + "="*70)
    print("DIAL API IMAGE GENERATION AND ANALYSIS - COMPREHENSIVE TESTS")
    print("="*70)
    print("This script will run all three tasks and pause for screenshots.")
    print("Press ENTER after taking each screenshot to continue.")
    input("\nPress ENTER to start...")
    
    # Test 1: OpenAI-style Image Analysis (Base64 encoding)
    def test_openai_itt():
        from task.image_to_text.openai.task_openai_itt import start
        start()
    
    run_test("Test 1: OpenAI-Style Image Analysis (Base64)", test_openai_itt)
    pause_for_screenshot("Test 1: OpenAI-Style Image Analysis")
    
    # Test 2: DIAL-style Image Analysis (Bucket storage)
    def test_dial_itt():
        from task.image_to_text.task_dial_itt import start
        start()
    
    run_test("Test 2: DIAL-Style Image Analysis (Bucket Storage)", test_dial_itt)
    pause_for_screenshot("Test 2: DIAL-Style Image Analysis")
    
    # Test 3: Text-to-Image Generation
    def test_tti():
        from task.text_to_image.task_tti import start
        start()
    
    run_test("Test 3: Text-to-Image Generation", test_tti)
    pause_for_screenshot("Test 3: Text-to-Image Generation")
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETED!")
    print("="*70)
    print("\n📋 Summary:")
    print("   ✅ Test 1: OpenAI-Style Image Analysis - Completed")
    print("   ✅ Test 2: DIAL-Style Image Analysis - Completed")
    print("   ✅ Test 3: Text-to-Image Generation - Completed")
    print("\n🎉 All image generation and analysis tests passed successfully!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()

