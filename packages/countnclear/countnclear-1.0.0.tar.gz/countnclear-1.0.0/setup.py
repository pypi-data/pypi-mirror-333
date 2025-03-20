from setuptools import setup, find_packages

setup(
    name="countnclear",  # PyPI’da paket nomi (pastki chiziq ishlatiladi)
    version="1.0.0",  # Paket versiyasi
    packages=find_packages(),  # Barcha paketlarni avtomatik topish
    description="A package to count terminal executions and clear the terminal after a specified limit",
    long_description=open("README.md").read(),  # README faylidan uzun tavsif
    long_description_content_type="text/markdown",  # README formati
    author="Raxmatullox",  # Muallif ismi
    author_email="raxmatulllox@icloud.com",  # Muallifning elektron pochta manzili
    url="https://github.com/raxmatullox/CountNClear",  # Loyiha repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimal Python versiyasi
    install_requires=[],  # Qo‘shimcha qaramliklar (hozircha yo‘q)
)