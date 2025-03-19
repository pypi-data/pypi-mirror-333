from setuptools import setup, find_packages

setup(
    name="bannerutils",
    version="1.1.1",
    author="@JfrzxCode",
    author_email="jfrzzzzzzz@gmail.com",
    description="Advanced ASCII Banner Generator.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jfrzz/bannerutils",  # Your GitHub repo
    packages=find_packages(),
    install_requires=[
        "pyfiglet",
        "pyperclip",
    ],
    entry_points={
        "console_scripts": [
            "banner=banner.bannerutils:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
