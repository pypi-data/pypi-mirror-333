from setuptools import setup, find_packages

setup(
    name="stitch_ai",
    version="0.1.4",
    description="Stitch AI SDK for managing memory spaces and memories",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Stitch AI",
    url="https://github.com/StitchAI/stitch-ai-cli-py",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "stitch=stitch_ai.sdk:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)