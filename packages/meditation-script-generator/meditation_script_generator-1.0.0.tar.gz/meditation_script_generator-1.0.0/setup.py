from setuptools import setup, find_packages

setup(
    name="meditation-script-generator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        # Currently only using standard library
    ],
    entry_points={
        'console_scripts': [
            'meditation-cli=meditation_generator:main',
            'meditation-gui=meditation_gui:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A meditation script generator with GUI and timer functionality",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="meditation, mindfulness, wellness, timer",
    url="https://github.com/yourusername/meditation-script-generator",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Lifestyle :: Wellness",
    ],
    python_requires=">=3.7",
) 