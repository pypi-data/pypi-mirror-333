import setuptools

setuptools.setup(
    name="pw-signal-processor",           
    version="0.1.2",
    author="PinkWink",
    author_email="pinkwink@pinklab.art",
    description="A simple library for moving average and 1st order low-pass filter",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pinklab-art/signal_processor", 
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
