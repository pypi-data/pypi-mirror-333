# setup.py
from setuptools import setup, find_packages

setup(
    name="user_manual",
    version="0.0.10",
    packages=find_packages(),
    install_requires= ["user-manual>=0.0.9"],    
    entry_points={
        'console_scripts': [
            'user_manual=user_manual.user_manual:main',
        ],
    },
    author="Aviral Srivastava",
    author_email="aviralsrivastava284@gmail.com",
    description="Generate the User Manual by ChatGPT",
    long_description_content_type='text/markdown',
    url="https://github.com/A284viral/protections_v1",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)