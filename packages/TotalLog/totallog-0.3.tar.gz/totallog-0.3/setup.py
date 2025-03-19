from setuptools import setup, find_packages

setup(
    name='TotalLog',  # Уникальное имя библиотеки
    version='0.3',
    packages=find_packages(),  # Автоматически находит пакеты в my_library/
    install_requires=[
        'colorama',
        'pycparser>=2.21',
        'datetime',
    ],
    author='Vanja Nazarenko',
    description='my own library for console logging',
)
