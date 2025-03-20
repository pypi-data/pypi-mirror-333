import setuptools

setuptools.setup(
    name="sikumim",
    version="0.1.4",
    author="Eitan Sztuden",
    description="A simple tool to download lecture notes, written by Regev Yehezkel Imra",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    py_modules=["download"],
    install_requires=["requests"],
    entry_points={"console_scripts": ["dl_lec=download:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
