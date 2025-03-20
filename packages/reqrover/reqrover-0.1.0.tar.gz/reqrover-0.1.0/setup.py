from setuptools import setup, find_packages

setup(
    name="req-rover",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
    ],
    entry_points="""
        [console_scripts]
        rover=rover.cli:cli
    """,
    author="n",
    description="A tool for discovering Python package dependencies",
    python_requires=">=3.6",
)
