from setuptools import setup, find_packages
# pip install wheel
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload dist/*

VERSION = '0.1.261'
DESCRIPTION = 'A basic science package'
LONG_DESCRIPTION = open('README.md').read()
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

setup(
    name="lhachimi",
    version=VERSION,
    author="Mohamed Lhachimi",
    author_email="mohamedyoutu123@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib', 'sympy', 'scipy' , 'requests' , 'scikit-learn'],
    keywords=['python', 'science', 'math', 'analysis', 'simplify science', 'programming'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
