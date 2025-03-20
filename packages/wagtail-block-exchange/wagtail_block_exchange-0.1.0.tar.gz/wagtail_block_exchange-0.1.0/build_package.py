#!/usr/bin/env python
"""
Helper script to build the wagtail-block-exchange package
with pre-built JavaScript files.
"""

import os
import subprocess
import shutil
import glob
import sys

def clean_dirs():
    """Clean up build directories."""
    print("Cleaning up old build directories...")
    for dir_name in ['dist', 'build', 'wagtail_block_exchange.egg-info']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

def build_js():
    """Build JavaScript files."""
    print("Building JavaScript files...")
    
    # Make sure the output directories exist
    os.makedirs('wagtail_block_exchange/static/wagtail_block_exchange/js/dist', exist_ok=True)
    os.makedirs('wagtail_block_exchange/static/wagtail_block_exchange/css', exist_ok=True)
    
    # Try to run npm build
    try:
        subprocess.check_call(['npm', 'install'], stdout=subprocess.PIPE)
        subprocess.check_call(['npm', 'run', 'build'], stdout=subprocess.PIPE)
        print("JavaScript built successfully.")
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        print(f"Warning: Failed to build JavaScript with npm: {e}")
        print("Using pre-built JavaScript files if available.")
    
    # Copy the built JS files to the package directory
    js_file = 'static/wagtail_block_exchange/js/dist/wagtail_block_exchange.js'
    if os.path.exists(js_file):
        dest = 'wagtail_block_exchange/' + js_file
        print(f"Copying {js_file} to {dest}")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(js_file, dest)
    else:
        print(f"Warning: Built JavaScript file {js_file} not found!")
    
    # Copy CSS files to the package directory
    css_file = 'static/wagtail_block_exchange/css/block-exchange.css'
    if os.path.exists(css_file):
        dest = 'wagtail_block_exchange/' + css_file
        print(f"Copying {css_file} to {dest}")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(css_file, dest)
    else:
        print(f"Warning: CSS file {css_file} not found!")

def build_package():
    """Build the Python package."""
    print("Building Python package...")
    
    # Use build module if available (more modern approach)
    try:
        subprocess.check_call([sys.executable, '-m', 'build'], 
                              stdout=subprocess.PIPE)
        print("Built package using build module")
    except subprocess.SubprocessError:
        # Fall back to setuptools directly
        print("Falling back to setuptools...")
        subprocess.check_call([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])

def check_dist():
    """Check if built distributions include required files."""
    print("Checking distributions...")
    
    # Check source dist
    sdist_files = glob.glob('dist/*.tar.gz')
    if sdist_files:
        sdist_file = sdist_files[0]
        print(f"Checking source distribution: {os.path.basename(sdist_file)}")
        result = subprocess.run(['tar', '-tvf', sdist_file], capture_output=True, text=True)
        if 'wagtail_block_exchange.js' in result.stdout:
            print(f"✅ Source distribution includes JavaScript files")
        else:
            print(f"❌ Source distribution is missing JavaScript files!")
    else:
        print("No source distribution found.")
    
    # Check wheel
    wheel_files = glob.glob('dist/*.whl')
    if wheel_files:
        wheel_file = wheel_files[0]
        print(f"Checking wheel: {os.path.basename(wheel_file)}")
        result = subprocess.run(['unzip', '-l', wheel_file], capture_output=True, text=True)
        if 'wagtail_block_exchange.js' in result.stdout:
            print(f"✅ Wheel includes JavaScript files")
        else:
            print(f"❌ Wheel is missing JavaScript files!")
    else:
        print("No wheel distribution found.")

def main():
    """Main entry point."""
    os.environ['SKIP_JS_BUILD'] = '1'  # Skip JS build in setup.py
    
    clean_dirs()
    build_js()
    build_package()
    check_dist()
    
    print("\nPackage build complete! Next steps:")
    print("---------------------------------------")
    print("To test locally:    pip install dist/*.whl")
    print("To upload to PyPI:  python -m twine upload dist/*")
    print("To upload to Test PyPI:  python -m twine upload --repository testpypi dist/*")

if __name__ == '__main__':
    main() 