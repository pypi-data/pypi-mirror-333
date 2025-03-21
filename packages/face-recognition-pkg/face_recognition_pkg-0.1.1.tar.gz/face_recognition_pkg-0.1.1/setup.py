from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Base requirements without FAISS
base_requirements = [
    "numpy",
    "opencv-python",
    "Pillow", 
    "sentence-transformers",
    "ultralytics",
    "supervision"
]

setup(
    name="face_recognition_pkg",
    version="0.1.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for face recognition in images and videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Anurich/face_recognition_package.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=base_requirements,
    extras_require={
        'cpu': ['faiss-cpu'],
        'gpu': ['faiss-gpu'],
    },
)