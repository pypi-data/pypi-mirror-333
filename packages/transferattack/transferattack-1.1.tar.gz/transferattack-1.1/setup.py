from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="transferattack",
    version="1.1", 
    author="Santhoshkumar K",
    author_email="santhoshatwork17@gmail.com",
    description="A PyTorch library for adversarial attacks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/santhosh1705kumar/transferattacks",
    # license="MIT",
    packages=find_packages(),  
    install_requires=[
        "torch>=1.9.0",
        "torchvision>=0.10.0",
        "numpy",
        "scipy",
        "tqdm",
        "matplotlib",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    include_package_data=True,  
    zip_safe=False,  
)
