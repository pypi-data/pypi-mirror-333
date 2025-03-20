from setuptools import setup, find_packages

try:
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    requirements = []

setup(
    name="chima_rufus",  
    version="0.2",  
    packages=find_packages(),
    install_requires=requirements,
    entry_points={  
        "console_scripts": [
            "mycrawler-api = mycrawler.api:app"
        ]
    },
    author='Mukesh Kumar Javvaji',
    author_email='mukeshjavvaji123@gmail.com'
)
