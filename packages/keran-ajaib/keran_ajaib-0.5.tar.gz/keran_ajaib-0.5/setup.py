from setuptools import setup, find_packages

with open("requirements.txt") as f:
    REQUIRE = f.read().splitlines()

setup(
    name='keran-ajaib',
    version='0.5',
    packages=find_packages(),
    install_requires=REQUIRE,
)