#!/usr/bin/env python3
"""Manual test script for deepseek-sdk package

This script verifies that the package can be imported and used correctly
after pip installation.
"""

import sys


def test_imports():
    """Test all package imports"""
    print("=" * 60)
    print("Testing Package Imports")
    print("=" * 60)
    
    try:
        from deepseek import DeepSeekClient, DeepSeekError, DeepSeekAPIError
        print("✓ Successfully imported: DeepSeekClient, DeepSeekError, DeepSeekAPIError")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_client_instantiation():
    """Test client creation"""
    print("\n" + "=" * 60)
    print("Testing Client Instantiation")
    print("=" * 60)
    
    try:
        from deepseek import DeepSeekClient
        
        # Test with default parameters
        client = DeepSeekClient(api_key="test_api_key")
        print("✓ Client created with default parameters")
        print(f"  - Default model: {client.default_model}")
        print(f"  - Base URL: {client.client.base_url}")
        
        # Test with custom parameters
        custom_client = DeepSeekClient(
            api_key="test_api_key",
            base_url="https://custom.api.com",
            default_model="custom-model"
        )
        print("✓ Client created with custom parameters")
        print(f"  - Custom model: {custom_client.default_model}")
        print(f"  - Custom base URL: {custom_client.client.base_url}")
        
        return True
    except Exception as e:
        print(f"✗ Client instantiation failed: {e}")
        return False


def test_client_methods():
    """Test that client has all expected methods"""
    print("\n" + "=" * 60)
    print("Testing Client Methods")
    print("=" * 60)
    
    try:
        from deepseek import DeepSeekClient
        
        client = DeepSeekClient(api_key="test_api_key")
        
        methods = [
            'chat_completion',
            'async_chat_completion',
            'stream_response',
            'async_stream_response'
        ]
        
        all_present = True
        for method in methods:
            has_method = hasattr(client, method)
            symbol = "✓" if has_method else "✗"
            print(f"{symbol} Method '{method}': {has_method}")
            if not has_method:
                all_present = False
        
        return all_present
    except Exception as e:
        print(f"✗ Method check failed: {e}")
        return False


def test_exceptions():
    """Test custom exception classes"""
    print("\n" + "=" * 60)
    print("Testing Custom Exceptions")
    print("=" * 60)
    
    try:
        from deepseek import DeepSeekError, DeepSeekAPIError
        
        # Test exception hierarchy
        assert issubclass(DeepSeekAPIError, DeepSeekError)
        assert issubclass(DeepSeekError, Exception)
        print("✓ Exception hierarchy correct")
        
        # Test raising exceptions
        try:
            raise DeepSeekError("Test error")
        except DeepSeekError as e:
            print(f"✓ DeepSeekError can be raised and caught: {e}")
        
        try:
            raise DeepSeekAPIError("Test API error")
        except DeepSeekAPIError as e:
            print(f"✓ DeepSeekAPIError can be raised and caught: {e}")
        
        return True
    except Exception as e:
        print(f"✗ Exception test failed: {e}")
        return False


def test_package_metadata():
    """Test package metadata"""
    print("\n" + "=" * 60)
    print("Testing Package Metadata")
    print("=" * 60)
    
    try:
        import deepseek
        
        if hasattr(deepseek, '__all__'):
            print(f"✓ Package exports: {deepseek.__all__}")
        
        if hasattr(deepseek, '__version__'):
            print(f"✓ Package version: {deepseek.__version__}")
        else:
            print("  Note: No __version__ attribute found (optional)")
        
        return True
    except Exception as e:
        print(f"✗ Metadata test failed: {e}")
        return False


def main():
    """Run all manual tests"""
    print("\n" + "=" * 60)
    print("DEEPSEEK-SDK MANUAL TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_client_instantiation,
        test_client_methods,
        test_exceptions,
        test_package_metadata
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test {test_func.__name__} crashed: {e}")
            results.append(False)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED! The package is working correctly.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
