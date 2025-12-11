from setuptools import setup, find_packages

setup(
    name="google-pagespeed-insights",
    version="1.0.0",
    description="Python package for Google PageSpeed Insights API",
    author="",
    author_email="",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
    ],
    python_requires=">=3.8",
)
