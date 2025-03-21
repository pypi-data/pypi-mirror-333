import os
import re
from setuptools import setup, find_packages

# Read version from __init__.py
with open(os.path.join("apifrom", "__init__.py"), "r") as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        version = "1.0.0"  # Default to 1.0.0 if not found

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = []
    for line in f:
        line = line.strip()
        # Skip comments, blank lines, and optional dependencies
        if line and not line.startswith("#") and ";" not in line:
            # Remove version specifiers
            req = line.split("==")[0].split(">=")[0].strip()
            requirements.append(req)

setup(
    name="apifrom",
    version=version,  # Use the extracted version
    author="Your Name",  # Update with your name
    author_email="your.email@example.com",  # Update with your email
    description="APIFromAnything: A flexible API framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/apifrom",  # Update with your repository URL
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/apifrom/issues",
        "Documentation": "https://apifrom.readthedocs.io/",
        "Source Code": "https://github.com/yourusername/apifrom",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Framework :: FastAPI",
    ],
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "flask": ["flask>=2.3.3"],
        "django": ["django>=4.2.10"],
        "all": ["flask>=2.3.3", "django>=4.2.10"],
    },
    entry_points={
        "console_scripts": [
            "apifrom=apifrom.cli:main",
        ],
    },
) 