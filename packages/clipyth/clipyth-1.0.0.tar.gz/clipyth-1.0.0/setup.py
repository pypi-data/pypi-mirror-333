from setuptools import setup

setup(
    name="clipyth",
    version="1.0.0",
    description="A simple CLI (Command Line Interface) to create python projects with different templates",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author="Elabsurdo984",
    author_email="matiassfernandez00@gmail.com",
    url="https://github.com/Elabsurdo984/clipyth.git",
    packages=["clipyth"],
    python_requires='>=3.8',
    license="MIT",
    entry_points={
        'console_scripts': [
            'clipyth=clipyth:main',
        ],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    project_urls={
        "Source": "https://github.com/Elabsurdo984/clipyth",
    }
)