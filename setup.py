import setuptools
import os

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="pyread",
    version="0.0.0a0",
    author="Jack Luby",
    author_email="jack.o.luby@gmail.com",
    description="Read selected .txt files aloud, storing progress.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    #package_data={'': ['helpers/config.json']},
    include_package_data=True,
    entry_points={
    'console_scripts': [f'{file[:-3]} = pyread.{file[:-3]}:main' for file in os.listdir("src/pyread") if file[-3:] == ".py"]
    }
)