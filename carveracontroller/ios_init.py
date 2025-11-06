"""
iOS initialization module - must be imported before pyobjus is used.
This patches pyobjus.dylib_manager to use correct iOS framework paths.
"""
import sys

def patch_pyobjus():
    """
    Monkey-patch pyobjus.dylib_manager to use correct iOS framework paths.
    This fixes the dlopen errors when loading frameworks on iOS.
    """
    if sys.platform != "ios":
        return

    try:
        # Import and patch pyobjus before it tries to load any frameworks
        import pyobjus.dylib_manager as dylib_manager
        from carveracontroller.ios_framework_loader import load_framework as custom_load_framework
        from carveracontroller.ios_framework_loader import load_dylib as custom_load_dylib
        from carveracontroller.ios_framework_loader import INCLUDE

        # Replace the functions in the module
        dylib_manager.load_framework = custom_load_framework
        dylib_manager.load_dylib = custom_load_dylib
        dylib_manager.INCLUDE = INCLUDE

        print("Successfully patched pyobjus.dylib_manager for iOS")
    except ImportError as e:
        print(f"Note: Could not patch pyobjus (not installed or not needed): {e}")
    except Exception as e:
        print(f"Warning: Failed to patch pyobjus.dylib_manager: {e}")

# Apply the patch when this module is imported
patch_pyobjus()
