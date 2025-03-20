from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup (
    name = 'wflite',
    version = '0.0.42',
    description = 'Workflow Lite: A lightweight workflow engine', 
    packages=find_packages(include=["wflite", "wflite.*"]),
    author = 'Jean-Paul Buu-Sao',
    author_email = 'jbuusao@jgmail.com',
    install_requires = [
        'requests',
        'pydantic',
        'python-dotenv'
    ],
    extras_require={
        'azure': [
            'azure-identity',
            'azure-keyvault-secrets'
        ],
    },
    entry_points={
        'console_scripts': [
            'wflite=wflite.cli.workflow_cli:main',
        ],
    },
    long_description = long_description,
    long_description_content_type = "text/markdown",
)
