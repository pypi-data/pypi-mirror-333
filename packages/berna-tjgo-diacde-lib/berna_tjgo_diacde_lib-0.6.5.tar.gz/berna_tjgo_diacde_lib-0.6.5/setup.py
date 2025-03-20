from setuptools import setup, find_packages

with open('berna_tjgo_diacde_lib/README.md', 'r', encoding='utf-8') as f:
    description = f.read()

setup(
    name='berna_tjgo_diacde_lib',
    version='0.6.5',
    author='TJGO - DIACDE',
    python_requires=">=3.9.4",
    requirements=[
        'pandas', 
        'spacy',
        'nltk', 
        ],
    license='Attribution-NonCommercial-ShareAlike',
    packages=find_packages(),
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/TJGO-DIACDE/berna_tjgo_diacde_lib',
)