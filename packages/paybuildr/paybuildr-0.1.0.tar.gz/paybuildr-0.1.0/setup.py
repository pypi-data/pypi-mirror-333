from setuptools import setup, find_packages
import os
import shutil

# Custom package finder that excludes node_modules
def find_packages_without_node_modules():
    packages = find_packages()
    return [pkg for pkg in packages if 'node_modules' not in pkg]

# Define a custom build class that removes node_modules from the build directory
from setuptools.command.build_py import build_py

class CustomBuildPy(build_py):
    def run(self):
        # Run the standard build first
        build_py.run(self)
        
        # Remove all node_modules directories from the build
        for package in self.packages:
            package_dir = os.path.join(self.build_lib, *package.split('.'))
            for root, dirs, files in os.walk(package_dir):
                if 'node_modules' in dirs:
                    node_modules_path = os.path.join(root, 'node_modules')
                    print(f"Removing {node_modules_path}")
                    shutil.rmtree(node_modules_path)

setup(
    name="paybuildr",
    version="0.1.0",
    packages=find_packages_without_node_modules(),
    include_package_data=True,
    install_requires=[
        "Django>=5.0.0",
        "djangorestframework>=3.14.0",
        "stripe>=7.0.0",
        "requests>=2.31.0",
    ],
    cmdclass={
        'build_py': CustomBuildPy,
    },
    author="James Munsch",
    author_email="james.munsch@ccsconsulting.rocks",
    description="A Django app for integrating Stripe payments and Kong API management",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/allen-munsch/paybuildr",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.12",
)