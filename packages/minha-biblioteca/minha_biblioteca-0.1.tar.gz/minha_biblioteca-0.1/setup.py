from setuptools import setup, find_packages

setup(
    name="minha_biblioteca",
    version="0.1",
    packages=find_packages(),
    description="Uma biblioteca de exemplo",
    author="Seu Nome",
    author_email="seu@email.com",
    url="https://github.com/seu_usuario/minha_biblioteca",  # Opcional
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
