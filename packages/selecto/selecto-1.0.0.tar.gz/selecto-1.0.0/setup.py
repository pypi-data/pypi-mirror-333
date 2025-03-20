from setuptools import setup, find_packages

setup(
    name="selecto",  
    version="1.0.0",  
    description="A TUI for selecting options easily with one function",
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",  
    author="Manuel Germanos",
    url="https://github.com/manuelgermanos/selecto",  
    packages=find_packages(),
    classifiers=[  
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: Microsoft :: Windows",  
    ],
    python_requires='>=3.6', 
    install_requires=[],  
)
