"""
Setup script for CreepyPasta AI
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="creepypasta-ai",
    version="1.0.0",
    author="CreepyPasta AI Team",
    description="AI-powered creepypasta story narration with atmospheric audio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/creepypastaAI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "creepypasta-ai=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["config/*.yaml", "assets/**/*"],
    },
)
