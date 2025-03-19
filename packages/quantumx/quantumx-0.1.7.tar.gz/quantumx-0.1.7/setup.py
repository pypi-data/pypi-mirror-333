from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys
import subprocess

class PostInstallCommand(install):
    """Custom post-installation tasks."""
    def run(self):
        install.run(self)  # Run the normal install process

        # Define the post-install action
        post_install_script = "quantumx.post_install"  # Module to run post-install
        post_install_message = "Running post-installation setup for QuantumX..."

        print(post_install_message)

        # Platform-specific execution
        if sys.platform.startswith("win"):
            try:
                # Check if running as admin (required for registry changes)
                if not hasattr(ctypes.windll.shell32, 'IsUserAnAdmin') or not ctypes.windll.shell32.IsUserAnAdmin():
                    print("Warning: Post-install script requires administrator privileges to register .qx file associations.")
                    print("Please re-run the installation with administrator rights or manually register .qx files.")
                else:
                    subprocess.call([sys.executable, "-m", post_install_script])  # Run as a module
                    print("Post-installation completed on Windows.")
            except subprocess.CalledProcessError as e:
                print(f"Warning: Post-install script failed on Windows: {e}")
            except ImportError:
                print(f"Warning: {post_install_script} module not found. Skipping post-install on Windows.")
        else:  # Linux, macOS, etc.
            print("No specific post-install action defined for this platform. Customize as needed.")

        print("QuantumX installation complete with post-install steps.")

setup(
    name="quantumx",
    version="0.1.7",
    packages=find_packages(),
    package_data={
        "quantumx": ["*.py", "icon.ico"],  # Include post_install.py and icon.ico
    },
    python_requires=">=3.8",  # Ensures compatibility with Python 3.8+
    install_requires=[        # List of package dependencies
        "numpy>=1.20",        # Add numpy as a dependency
        "pandas>=1.3.0",      # Add pandas as a dependency
    ],
    cmdclass={
        "install": PostInstallCommand,  # Run custom install command
    },
    entry_points={
        "console_scripts": [
            "quantumx = quantumx.interpreter:main"
        ]
    },
    author="Dhanush Selvaraj",
    author_email="sdhanush451@gmail.com",
    description="A quantum-inspired programming language",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dhanushs005/quantumx",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)