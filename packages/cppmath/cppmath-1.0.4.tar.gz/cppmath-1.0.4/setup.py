from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cppmath",
    version="1.0.4",
    author="mathercpp",
    author_email="",
    description="C++",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['cppmath'],
    package_dir={'cppmath': 'obf_cppmath/cppmath'},
    package_data={
        'cppmath': ['__pyarmor__/*.*', '*.py', '*.pyd']
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.0",
        "requests>=2.25.0",
    ],
)