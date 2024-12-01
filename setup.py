from setuptools import setup, find_packages

setup(
    name="meu_projeto",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=2.3",
        "mysql-connector-python>=8.0",
        "flask-cors" 
    ],
    extras_require={
        "dev": ["pytest", "mypy"]
    },
)
