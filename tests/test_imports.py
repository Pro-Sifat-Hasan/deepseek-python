"""Test that the package imports work correctly after installation"""
import pytest


class TestImports:
    """Test package imports"""

    def test_import_main_package(self):
        """Test importing the main package"""
        import deepseek
        assert deepseek is not None

    def test_import_client(self):
        """Test importing DeepSeekClient"""
        from deepseek import DeepSeekClient
        assert DeepSeekClient is not None

    def test_import_errors(self):
        """Test importing error classes"""
        from deepseek import DeepSeekError, DeepSeekAPIError
        assert DeepSeekError is not None
        assert DeepSeekAPIError is not None

    def test_all_exports(self):
        """Test __all__ exports"""
        import deepseek
        assert hasattr(deepseek, '__all__')
        assert 'DeepSeekClient' in deepseek.__all__
        assert 'DeepSeekError' in deepseek.__all__
        assert 'DeepSeekAPIError' in deepseek.__all__

    def test_module_attributes(self):
        """Test that imported module has expected attributes"""
        from deepseek import DeepSeekClient
        
        # Check that the class has expected methods
        assert hasattr(DeepSeekClient, 'chat_completion')
        assert hasattr(DeepSeekClient, 'async_chat_completion')
        assert hasattr(DeepSeekClient, 'stream_response')
        assert hasattr(DeepSeekClient, 'async_stream_response')

    def test_direct_module_import(self):
        """Test importing from deepseek.deepseek module"""
        from deepseek.deepseek import DeepSeekClient, DeepSeekError, DeepSeekAPIError
        assert DeepSeekClient is not None
        assert DeepSeekError is not None
        assert DeepSeekAPIError is not None
