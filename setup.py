#!/usr/bin/env python3
"""
Setup script for Certificate Generator
This script helps users prepare their environment for certificate generation.
"""

import os
import sys

def check_requirements():
    """Check if required tools are available."""
    print("Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6+ is required")
        return False
    else:
        print("✅ Python version:", sys.version.split()[0])
    
    # Check for XeLaTeX
    try:
        import subprocess
        result = subprocess.run(["xelatex", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ XeLaTeX is available")
        else:
            print("❌ XeLaTeX not found")
            return False
    except FileNotFoundError:
        print("❌ XeLaTeX not found. Please install a LaTeX distribution:")
        print("   - macOS: Install MacTeX")
        print("   - Windows: Install MiKTeX")
        print("   - Linux: Install TeX Live")
        return False
    
    return True

def create_sample_files():
    """Create sample files for testing."""
    print("\nCreating sample files...")
    
    # Create sample CSV if it doesn't exist
    if not os.path.exists("sample_names.csv"):
        with open("sample_names.csv", "w") as f:
            f.write("Lastname,Name,completion_date\n")
            f.write("Lincoln,Abraham,1809-02-12\n")
            f.write("King,Martin Luther,1929-01-15\n")
            f.write("Mandela,Nelson,1918-07-18\n")            
        print("✅ Created sample_names.csv")
    else:
        print("✅ sample_names.csv already exists")
    
    # Create output directories if they don't exist
    output_dirs = ["output", "output/pdfs", "output/tex"]
    for dir_path in output_dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"✅ Created {dir_path}/ directory")
        else:
            print(f"✅ {dir_path}/ directory already exists")

def print_next_steps():
    """Print instructions for next steps."""
    print("\n" + "="*50)
    print("SETUP COMPLETE!")
    print("="*50)
    print("\nNext steps:")
    print("1. Add your background image as 'certificate_base_page.png'")
    print("2. Create your participant data file as 'names.csv'")
    print("3. Customize the certificate content in 'generate_certificates.py'")
    print("4. Run: python3 generate_certificates.py")
    print("\nFor more information, see README.md")

def main():
    """Main setup function."""
    print("Certificate Generator Setup")
    print("="*30)
    
    if check_requirements():
        create_sample_files()
        print_next_steps()
    else:
        print("\n❌ Setup failed. Please install missing requirements.")
        sys.exit(1)

if __name__ == "__main__":
    main() 