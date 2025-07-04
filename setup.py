#!/usr/bin/env python3
"""
Machine Learning Course Setup Script
This script helps students set up their environment for the ML course.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Error installing packages. Please check your internet connection and try again.")
        return False
    return True

def verify_installation():
    """Verify that key packages are installed correctly"""
    print("\n🔍 Verifying installation...")
    
    required_packages = [
        'numpy', 'pandas', 'matplotlib', 'seaborn', 
        'sklearn', 'jupyter', 'scipy'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            else:
                __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError:
            print(f"❌ Failed to import {package}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n⚠️ Some packages failed to import: {failed_imports}")
        print("Please try running: pip install --upgrade " + " ".join(failed_imports))
        return False
    
    print("\n🎉 All packages verified successfully!")
    return True

def create_jupyter_config():
    """Create basic Jupyter configuration"""
    print("\n📝 Setting up Jupyter configuration...")
    
    # Create a simple notebook with welcome message
    welcome_notebook = """
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Welcome to Machine Learning Course! 🚀\\n",
    "\\n",
    "If you can see this notebook, your environment is set up correctly!\\n",
    "\\n",
    "## Quick Test\\n",
    "Run the cell below to test your installation:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Test basic imports\\n",
    "import numpy as np\\n",
    "import pandas as pd\\n",
    "import matplotlib.pyplot as plt\\n",
    "import seaborn as sns\\n",
    "from sklearn.datasets import load_iris\\n",
    "\\n",
    "print('🎉 All imports successful!')\\n",
    "print('✅ You are ready to start the ML course!')\\n",
    "\\n",
    "# Quick visualization test\\n",
    "x = np.linspace(0, 10, 100)\\n",
    "y = np.sin(x)\\n",
    "\\n",
    "plt.figure(figsize=(8, 4))\\n",
    "plt.plot(x, y)\\n",
    "plt.title('Environment Test - Sine Wave')\\n",
    "plt.xlabel('x')\\n",
    "plt.ylabel('sin(x)')\\n",
    "plt.grid(True, alpha=0.3)\\n",
    "plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
"""
    
    try:
        with open("test_environment.ipynb", "w") as f:
            f.write(welcome_notebook)
        print("✅ Created test_environment.ipynb")
    except Exception as e:
        print(f"❌ Error creating test notebook: {e}")

def print_next_steps():
    """Print instructions for getting started"""
    print("\n" + "="*60)
    print("🎓 MACHINE LEARNING COURSE SETUP COMPLETE!")
    print("="*60)
    print("\n📚 Next Steps:")
    print("1. Start Jupyter Notebook: jupyter notebook")
    print("2. Open 'test_environment.ipynb' to verify everything works")
    print("3. Begin with Chapter 1: chapters/chapter_01_introduction_to_ml.ipynb")
    print("4. Read the course guide: resources/course_guide.md")
    print("\n💡 Tips:")
    print("- Complete chapters sequentially (1-10)")
    print("- Run all code examples and modify them")
    print("- Complete exercises at the end of each chapter")
    print("- Use the sample datasets in the 'datasets/' folder")
    print("\n🚀 Happy Learning!")
    print("="*60)

def main():
    """Main setup function"""
    print("🎓 Machine Learning Course Setup")
    print("="*40)
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found. Please ensure you're in the correct directory.")
        return
    
    # Install packages
    if not install_requirements():
        return
    
    # Verify installation
    if not verify_installation():
        return
    
    # Create Jupyter config
    create_jupyter_config()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()