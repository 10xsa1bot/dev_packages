from setuptools import setup

setup(
    name="google-pagespeed-insights",
    version="1.0.0",
    description="Python package for Google PageSpeed Insights API",
    author="",
    author_email="",
    packages=["google_pagespeed_insights"],
    package_dir={"google_pagespeed_insights": "src"},
    install_requires=[
        "requests>=2.31.0",
    ],
    python_requires=">=3.8",
)
