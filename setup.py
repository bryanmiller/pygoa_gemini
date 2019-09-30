import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pygoa-gemini',
    version='1.0.0',
    author="Bryan Miller",
    author_email="millerwbryan@gmail.com",
    description="A simple python library for working with the Gemini Observatory Archive APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bryanmiller/pygoa",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    keywords=['astronomy', 'astrophysics', 'science', 'fits', 'observatory', 'gemini', 'archive'],
    install_requires=[
        'requests',
    ]
)