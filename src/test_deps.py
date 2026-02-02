"""
Test Dependencies
=================
Check if all required dependencies are installed.
"""

import sys

def test_import(module_name, package_name=None):
    """Test if a module can be imported."""
    try:
        __import__(module_name)
        print(f"✅ {package_name or module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name or module_name} - NOT INSTALLED")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {package_name or module_name} - ERROR")
        print(f"   Error: {e}")
        return False

def main():
    print("="*60)
    print("Testing Dependencies")
    print("="*60)
    print()
    
    results = []
    
    # Test core dependencies
    print("Core Dependencies:")
    results.append(test_import("whisper", "openai-whisper"))
    results.append(test_import("sounddevice"))
    results.append(test_import("numpy"))
    results.append(test_import("pyautogui"))
    results.append(test_import("keyboard"))
    
    print()
    print("New Dependencies (Cursor Tracking):")
    results.append(test_import("win32api", "pywin32"))
    results.append(test_import("pystray"))
    results.append(test_import("PIL", "pillow"))
    
    print()
    print("Python Built-in:")
    results.append(test_import("tkinter"))
    results.append(test_import("winsound"))
    
    print()
    print("="*60)
    if all(results):
        print("✅ All dependencies installed!")
        print("="*60)
        return 0
    else:
        print("❌ Some dependencies missing!")
        print("="*60)
        print()
        print("To install missing dependencies:")
        print("  pip install -r requirements.txt")
        print("  Or run: install_new_deps.bat")
        return 1

if __name__ == "__main__":
    sys.exit(main())
