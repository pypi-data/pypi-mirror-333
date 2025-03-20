from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import subprocess
import os
import sys
import glob
import shutil

with open("README.md", "r") as fh:
    long_description = fh.read()

class BuildWithJS(build_py):
    """Custom build command that builds JavaScript assets before Python package."""
    
    def run(self):
        # Only build if we're creating a distribution
        if os.environ.get('SKIP_JS_BUILD') != '1':
            self.build_javascript()
            
        # Ensure the output directories exist
        os.makedirs('wagtail_block_exchange/static/wagtail_block_exchange/js/dist', exist_ok=True)
        os.makedirs('wagtail_block_exchange/static/wagtail_block_exchange/css', exist_ok=True)
        
        # Copy the built JS files to the package directory
        js_file = 'static/wagtail_block_exchange/js/dist/wagtail_block_exchange.js'
        if os.path.exists(js_file):
            dest = 'wagtail_block_exchange/' + js_file
            print(f"Copying {js_file} to {dest}")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(js_file, dest)
        
        # Copy CSS files to the package directory
        css_file = 'static/wagtail_block_exchange/css/block-exchange.css'
        if os.path.exists(css_file):
            dest = 'wagtail_block_exchange/' + css_file
            print(f"Copying {css_file} to {dest}")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(css_file, dest)
            
        # Call the original build_py
        build_py.run(self)
    
    def build_javascript(self):
        """Build the JavaScript assets."""
        print("Building JavaScript assets...")
        
        # Record the current directory
        current_dir = os.getcwd()
        
        try:
            # Change to the package directory if needed
            package_dir = os.path.abspath(os.path.dirname(__file__))
            os.chdir(package_dir)
            
            # Check if npm is available
            try:
                subprocess.check_call(['npm', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except (subprocess.SubprocessError, FileNotFoundError):
                print("Warning: npm not found. Using pre-built JavaScript files if available.")
                return
            
            # Install dependencies
            subprocess.check_call(['npm', 'install'], stdout=subprocess.PIPE)
            
            # Build the JavaScript
            subprocess.check_call(['npm', 'run', 'build'], stdout=subprocess.PIPE)
            
            print("JavaScript assets built successfully.")
        except subprocess.SubprocessError as e:
            print(f"Error building JavaScript assets: {e}")
            print("Continuing with installation using pre-built assets if available.")
        finally:
            # Restore the original directory
            os.chdir(current_dir)

# Find all files in specified directories to include in package_data
def find_package_data(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

# Create a list of all files in the static directory
static_files = find_package_data('wagtail_block_exchange/static')
template_files = find_package_data('wagtail_block_exchange/templates')

setup(
    name="wagtail-block-exchange",
    version="0.1.0",
    author="Rich Ross",
    author_email="rich@welovemicro.com",
    description="A Wagtail plugin to copy and paste blocks between pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/welovemicro/wagtail-block-exchange",
    project_urls={
        "Bug Tracker": "https://gitlab.com/welovemicro/wagtail-block-exchange/-/issues",
        "Documentation": "https://gitlab.com/welovemicro/wagtail-block-exchange/-/blob/main/README.md",
        "Source Code": "https://gitlab.com/welovemicro/wagtail-block-exchange",
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['LICENSE', 'README.md'],
        'wagtail_block_exchange': static_files + template_files,
    },
    data_files=[
        ('static/wagtail_block_exchange/js/dist', ['static/wagtail_block_exchange/js/dist/wagtail_block_exchange.js']),
        ('static/wagtail_block_exchange/css', ['static/wagtail_block_exchange/css/block-exchange.css']),
    ],
    cmdclass={
        'build_py': BuildWithJS,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 4",
        "Framework :: Wagtail :: 5",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.8",
    install_requires=[
        "wagtail>=4.1",
        "django>=3.2",
    ],
) 