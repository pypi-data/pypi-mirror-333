from setuptools import setup, find_packages

setup(
    name="african-knowledge-ai",
    version="0.1.0",
    description="Python SDK for African Knowledge AI API",
    author="Your Name",
    author_email="your-email@example.com",
    url="https://github.com/yourusername/african-knowledge-ai-sdk",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
