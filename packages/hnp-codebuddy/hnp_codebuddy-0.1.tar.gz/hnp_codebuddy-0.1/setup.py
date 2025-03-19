from setuptools import setup, find_packages

setup(
    name="hnp-codebuddy",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "cr-bot=hnp_codebuddy.cli:review_pr"
        ]
    }
)
