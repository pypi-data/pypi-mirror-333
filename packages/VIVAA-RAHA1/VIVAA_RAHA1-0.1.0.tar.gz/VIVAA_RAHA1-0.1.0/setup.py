from setuptools import setup, find_packages

setup(
    name="VIVAA_RAHA1",
    version="0.1.0",
    author="VISHNU_VARDHAN",
    author_email="vardhan101101@gmail.com",
    description="A description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "FreeSimpleGUI",
        "opencv-python",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'viva=VIVA.maaain:main',
        ],
    },
)