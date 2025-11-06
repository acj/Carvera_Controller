"""
Custom iOS framework loader to replace pyobjus.dylib_manager.load_framework
which uses incorrect macOS-style paths on iOS.
"""
import ctypes
import os

_loaded_frameworks = {}

def load_framework(framework_path):
    """
    Load an iOS framework using the correct path structure.

    iOS frameworks use a simple structure:
    /System/Library/Frameworks/FrameworkName.framework/FrameworkName

    Unlike macOS which has:
    /System/Library/Frameworks/FrameworkName.framework/Versions/Current/FrameworkName

    Args:
        framework_path: Path to the framework (e.g., '/System/Library/Frameworks/UIKit.framework')

    Returns:
        The loaded framework CDLL object
    """
    if framework_path in _loaded_frameworks:
        return _loaded_frameworks[framework_path]

    # Extract the framework name from the path
    # e.g., '/System/Library/Frameworks/UIKit.framework' -> 'UIKit'
    framework_name = os.path.basename(framework_path).replace('.framework', '')

    # Construct the correct iOS framework binary path
    binary_path = os.path.join(framework_path, framework_name)

    try:
        # Try loading with the direct path
        framework = ctypes.CDLL(binary_path)
        _loaded_frameworks[framework_path] = framework
        print(f"Successfully loaded framework: {binary_path}")
        return framework
    except OSError as e:
        # If direct path fails, try without the full path (let the system find it)
        try:
            framework = ctypes.CDLL(framework_name + ".framework/" + framework_name)
            _loaded_frameworks[framework_path] = framework
            print(f"Successfully loaded framework using short path: {framework_name}")
            return framework
        except OSError:
            # Last resort: let the dynamic linker find it
            try:
                framework = ctypes.CDLL(None)  # Load main bundle, which has access to all frameworks
                _loaded_frameworks[framework_path] = framework
                print(f"Using main bundle for framework: {framework_name}")
                return framework
            except Exception as final_error:
                print(f"Failed to load framework {framework_path}: {e}")
                raise

def load_dylib(dylib_path):
    """
    Load a dynamic library.

    Args:
        dylib_path: Path to the dylib

    Returns:
        The loaded CDLL object
    """
    return ctypes.CDLL(dylib_path)

# Constants for compatibility with pyobjus
INCLUDE = ctypes.DEFAULT_MODE
