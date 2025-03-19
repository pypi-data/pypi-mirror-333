from setuptools import setup, find_packages

setup(
    name="yoptapy",
    version="0.1.1",
    description="Гоп-язык для Python",
    long_description=open("README.md").read() if open("README.md", encoding="utf-8") else "",
    long_description_content_type="text/markdown",
    author="Твой Имя",
    author_email="твой@email.com",
    url="https://github.com/твой_репозиторий",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "yoptapy = yoptapy.yoptapy:main" 
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)