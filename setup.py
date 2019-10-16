import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='cary_reader',  
    version='0.3',
    author="Ivo Herzig",
    author_email="hezi@zhaw.ch",
    description="Reads and processes Agilent Cary Eclipse Spectrophotometer csv files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
	install_requires=[
		'pandas'
	],
    packages=setuptools.find_packages(),
    classifiers=[
            "License :: OSI Approved :: MIT License",
            "Development Status :: 2 - Pre-Alpha", 
            "Topic :: Scientific/Engineering :: Chemistry"
            ],
 )
