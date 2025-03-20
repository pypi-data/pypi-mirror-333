from setuptools import setup, find_packages

setup(
    name="library_manager_ausaf",  # Your package name
    version="0.2",  # Package version
    packages=find_packages(),  
    install_requires=[
        "pyfiglet", "inquirer", "tabulate", "yaspin", "colorama", "termcolor"  
    ],
    entry_points={
        "console_scripts": [
            "library-manager = library_manager.library_manager:main",
        ],
    },
    author="Ausaf Ul Islam",
    author_email="ausafkhan7777@gmail.com",
    description="A powerful and easy-to-use Python library for managing your personal book collection effortlessly. Add, search, track, and organize your books with a simple command-line interface.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ausafulislam/library_manager",
    classifiers=[  
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  
)
