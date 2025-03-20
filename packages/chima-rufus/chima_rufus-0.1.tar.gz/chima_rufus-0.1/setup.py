from setuptools import setup, find_packages

setup(
    name="chima_rufus",  
    version="0.1",  
    packages=find_packages(),
    install_requires=[  
        "requests",
        "beautifulsoup4",
        "fastapi",
        "uvicorn"
    ],
    entry_points={  
        "console_scripts": [
            "mycrawler-api = mycrawler.api:app"
        ]
    },
    author='Mukesh Kumar Javvaji',
    author_email='mukeshjavvaji123@gmail.com'
)
