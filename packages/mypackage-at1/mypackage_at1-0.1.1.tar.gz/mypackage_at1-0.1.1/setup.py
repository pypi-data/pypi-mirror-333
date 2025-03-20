from setuptools import setup, find_packages


setup(
    name='mypackage_at1',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[],
    author="Annie Thomas",
    author_email="annie.thomas1@ibm.com",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.ibm.com/ANNIE-THOMAS1/sample_building_blocks",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)