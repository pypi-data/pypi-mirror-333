from setuptools import setup, find_packages

setup(
    name="imagetoolkit",
    version="0.1.0",
    description="Advanced tool for processing images from the command line",
    author="jedahee",
    author_email="jdaza.her@gamil.com",
    url="https://github.com/jedahee/imagetoolkit",  # Update if you have a repo, or remove if not needed
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "Pillow==11.0.0",
        "prompt==0.4.1",
        "prompt-toolkit==3.0.36",
        "Pygments==2.18.0",
        "questionary==2.0.1",
        "regex==2024.11.6",
        "setuptools==75.8.0",
        "six==1.16.0",
        "wcwidth==0.2.13"
    ],
    entry_points={
        "console_scripts": [
            "imagetoolkit=imagetoolkit.imagetoolkit:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    license="Creative Commons Legal Code"
)
