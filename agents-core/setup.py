#!/usr/bin/env python3
"""
Setup script for the agents_core project.

This script helps configure the development environment.
"""

import os
import sys
import subprocess
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.absolute()


def install_package_in_development_mode():
    """Install the package in development mode."""
    project_root = get_project_root()
    print(f"Installing package in development mode from: {project_root}")
    
    try:
        # Install in editable mode
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                      cwd=project_root, check=True)
        print("✅ Package installed successfully in development mode!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install package: {e}")
        return False


def check_python_path():
    """Check if the current directory is in PYTHONPATH."""
    project_root = str(get_project_root())
    python_path = os.environ.get('PYTHONPATH', '')
    
    print(f"Project root: {project_root}")
    print(f"Current PYTHONPATH: {python_path}")
    
    if project_root in python_path:
        print("✅ Project root is in PYTHONPATH")
        return True
    else:
        print("⚠️  Project root is NOT in PYTHONPATH")
        print(f"To add it temporarily, run:")
        print(f"export PYTHONPATH=\"{project_root}:$PYTHONPATH\"")
        return False


def test_import():
    """Test if the package can be imported."""
    try:
        import agents_core
        from agents_core import DummyAgent
        print("✅ Package imports successfully!")
        print(f"Package version: {agents_core.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import package: {e}")
        return False


def main():
    """Main setup function."""
    print("=== agents_core Project Setup ===\n")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}\n")
    
    # Check current directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script directory: {get_project_root()}\n")
    
    # Option 1: Install in development mode (recommended)
    print("Option 1: Installing package in development mode...")
    if install_package_in_development_mode():
        print("Testing import after installation...")
        if test_import():
            print("\n🎉 Setup completed successfully!")
            print("You can now run: python example.py")
        else:
            print("\n❌ Setup failed - import test failed")
    else:
        print("\nOption 2: Using PYTHONPATH...")
        check_python_path()
        print("\nTo test manually, try:")
        print("python -c 'from agents_core import DummyAgent; print(\"Import successful!\")'")


if __name__ == "__main__":
    main()
