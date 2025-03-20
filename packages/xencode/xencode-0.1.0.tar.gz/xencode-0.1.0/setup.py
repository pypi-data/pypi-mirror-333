from setuptools import setup, find_packages

setup(
    name="xencode",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'xc=xencode.scripts.xc:main',
        ],
    },
    install_requires=[],
    author="Tu Nombre",
    author_email="tu.email@example.com",
    description="XEncode: Un fork de JavaScript junto a Python",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/tuusuario/xencode",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
