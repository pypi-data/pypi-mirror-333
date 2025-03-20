import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UOPython",
    version="0.2.0",
    author="JBob",
    author_email="thatdudejbob@gmail.com",
    description="UOPython - Extract information and images from the UO client files. New Fork from jackuolls ultima-py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NerdyGamers/UOPython",
    packages=setuptools.find_packages(),
    license="Beerware",
    install_requires=[
        'Pillow',
        'imageio',
        'numpy',
        'matplotlib'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: Freeware",
        "Development Status :: 4 - Beta",
    ],
)
