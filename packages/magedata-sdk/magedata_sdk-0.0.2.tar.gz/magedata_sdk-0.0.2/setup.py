from setuptools import setup, find_packages

setup(
   name="magedata_sdk",
   version="0.0.2",
   packages=find_packages(),
   install_requires=[
        "requests>=2.25.0",
        "jsonpath-ng>=1.5.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0"
   ],
   author="Mage Data",
   author_email="info@magedata.ai",
   description="Mage Data SDK for data anonymization",
   long_description=open("README.md").read(),
   long_description_content_type="text/markdown",
   url="https://github.com/mage-data/magedata_sdk",
   license="Proprietary",
   classifiers=[
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
   ],
   python_requires=">=3.8"
)
