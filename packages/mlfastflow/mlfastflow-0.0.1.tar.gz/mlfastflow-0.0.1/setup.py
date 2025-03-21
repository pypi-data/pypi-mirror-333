from setuptools import setup, find_packages

setup(
    name="mlfastflow",
    version="0.0.1",
    author="Xileven",
    author_email="hi@bringyouhome.com",
    description="packages for fast dataflow and workflow processing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xileven/mlfastflow",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pandas",
        "numpy",
        "faiss-cpu",
    ],
    package_data={
        '': ['README.md'],
    },
    project_urls={
        'Documentation': 'https://github.com/xileven/mlfastflow',
        'Source': 'https://github.com/xileven/mlfastflow',
        'Tracker': 'https://github.com/xileven/mlfastflow/issues',
    },
)
