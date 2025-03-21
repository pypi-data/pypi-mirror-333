from setuptools import setup, find_packages

setup(
    name="latex_lib",
    version="0.1.0",
    author="Igor Makarov",
    author_email="realneiro@gmail.com",
    description="Генератор LaTeX таблиц и LaTeX картинок",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Qeshtir/ITMO_Advanced_Python/hw_2/latex_lib",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)