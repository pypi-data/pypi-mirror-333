from setuptools import setup, find_packages

setup(
    name="SST4",
    version="0.1",
    author="HUSSAIN-HAEDER",
    author_email="reco9678785@gmail.com",
    description="*",
    packages=find_packages(),
    install_requires=[
        "user_agent",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
        
    ],
    python_requires=">=3.6",
)