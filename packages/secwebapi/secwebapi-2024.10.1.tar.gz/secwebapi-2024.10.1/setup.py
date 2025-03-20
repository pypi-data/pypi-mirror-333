from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="secwebapi",
    version="2024.10.1",
    description="A Python package to interact with the Secwe API",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://secwe.pythonanywhere.com",
    author="Samet Azaboglu",
    author_email="sametazaboglu@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tldextract",
        "aiohttp"
    ],
)