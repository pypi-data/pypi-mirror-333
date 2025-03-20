from setuptools import setup, find_packages

setup(
    name="xbeastx",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "Telethon",
        "APScheduler",
        "requests",
        "pytz",
        "pyrogram",
        "pymongo",
        "colorama",
        "localdb.json",
        "lolpy",
    ],
    description="A package that imports all required dependencies.",
    author="Your Name",
    author_email="atronpay7@gmail.com",
    url="https://github.com/msy1717/xbeastx",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
