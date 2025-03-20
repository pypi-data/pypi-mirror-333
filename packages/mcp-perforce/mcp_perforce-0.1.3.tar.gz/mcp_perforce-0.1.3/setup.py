from setuptools import setup, find_packages

setup(
    name="mcp-perforce",
    version="0.1.3",
    description="mcp-perforce",
    packages=find_packages(),
    install_requires=[
        "requests",
        "bs4",
        "mcp",
    ],
    entry_points={
        "console_scripts": [
            "mcp-perforce = mcp_perforce:main",
        ],
    },
)