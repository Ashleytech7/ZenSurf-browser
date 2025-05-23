from setuptools import setup, find_packages

setup(
    name="ZenSurf",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        'PyQtWebEngine',
    ],
    entry_points={
        'console_scripts': [
            'zensurf=main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A modern web browser built with PyQt5",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/zensurf",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
) 