"""
Setup per Email Optimizer
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="email-optimizer",
    version="1.0.0",
    author="Your Name",
    description="Agente AI per l'analisi intelligente delle email",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/email-optimizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Email",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "anthropic>=0.39.0",
        "google-api-python-client>=2.100.0",
        "google-auth-httplib2>=0.1.1",
        "google-auth-oauthlib>=1.1.0",
        "imapclient>=3.0.1",
        "email-validator>=2.1.0",
        "python-dateutil>=2.8.2",
        "beautifulsoup4>=4.12.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "rich>=13.7.0",
        "tinydb>=4.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "email-optimizer=main:main",
        ],
    },
)
