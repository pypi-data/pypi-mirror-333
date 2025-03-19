from setuptools import setup, find_packages

setup(
    name="pyescher",
    version="0.2.2",
    description="A Matplotlib wrapper that easily generates very scientific looking plots",
    author="Robert Fennis",
    author_email="fennisrobert@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],  # Add dependencies here

    # ✅ Fix license issue (use `license` instead of `license-file`)
    license="MIT",  # Make sure this matches the classifier

    # ✅ Add classifiers for PyPI compatibility
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],

    # ✅ Include non-Python files if needed
    include_package_data=True,
    package_data={"pyescher": ["*.txt", "*.csv"]},  # Adjust if needed
)
