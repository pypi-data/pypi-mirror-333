from setuptools import setup, find_packages

setup(
    name="termstyler",  # Package name
    version="2.1.1",  # Initial version
    author="NotHerXenon",
    author_email="rifatarefinchowdhury@gmail.com",
    description="A terminal styling library with colors, backgrounds, and text effects",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
