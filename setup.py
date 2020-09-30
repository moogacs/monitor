import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="website-monitor",
    version="0.0.1",
    author="Mohamed Badawi",
    author_email="contact@m-mooga.com",
    description="Websites monitoring system using Kafka, PSQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moogacs/monitor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)