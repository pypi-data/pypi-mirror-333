from setuptools import setup, find_packages

setup(
    name="gerador_tabuada",  # Nome do pacote
    version="0.1",  # Versão do pacote
    packages=find_packages(),  # Inclui todas as pastas que contêm pacotes
    install_requires=[],  # Caso tenha dependências externas, adicione aqui
    entry_points={
        'console_scripts': [
            'gerador-tabuada=gerador_tabuada.tabuada:main',  # Define a função 'main' como ponto de entrada
        ],
    },
)
