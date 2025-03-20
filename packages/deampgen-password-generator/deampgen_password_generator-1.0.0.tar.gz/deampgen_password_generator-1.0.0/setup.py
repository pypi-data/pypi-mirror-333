from setuptools import setup, find_packages
setup(
    name="deampgen_password_generator",  # Уникальное имя пакета
    version="1.0.0",                     # Версия пакета
    author="Sergey",                  # Автор
    description="A simple password generator library",
    packages=find_packages(),            # Автоматический поиск пакетов
    classifiers=[                        # Классификаторы для PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)