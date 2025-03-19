from setuptools import setup, find_packages

setup(
    name="cus_depr",          # Название пакета
    version="0.0.1",                    # Версия пакета
    packages=find_packages(),         # Все папки с кодом, в которых есть __init__.py
    description="A simple deprecation decorator",  # Описание пакета
    author="Андрей",
    author_email="danya10121985@gmail.com", # Твой email
    classifiers=[                   # Классификаторы пакета
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6, <3.13',         # Требования к версии Python
)
