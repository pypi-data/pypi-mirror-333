from setuptools import setup, find_packages

setup(
    name="rpa_hub",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Christian Schmitz Barbosa",
    description="Biblioteca em python para a integração dos RPAs com o sistema RPA-HUB",
    url="https://github.com/creditoreal-hub/RPA-Hub-Biblioteca",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
