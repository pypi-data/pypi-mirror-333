from setuptools import setup, find_packages

setup(
    name="mergerz",
    version="4.0.0",
    author="Afnan Tawsif",
    author_email="afnantawsif778@gmail.com",
    description="Blazingly fast module to merge PDFs and slides.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    package_data={"mergerz": ["*.pyd"]},  # Include all .pyd files
    include_package_data=True,  # Ensures MANIFEST.in is used
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    install_requires=[
        "reportlab>=4.3.1",
        "pillow>=11.1.0",
        "pymupdf>=1.25.3",
        "colorama>=0.4.6",
        "natsort>=8.4.0",
        "pikepdf>=9.5.2"
    ]
)