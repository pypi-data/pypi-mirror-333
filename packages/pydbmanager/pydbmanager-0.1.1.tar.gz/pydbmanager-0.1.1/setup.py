from setuptools import setup, find_packages

setup(
    name="pydbmanager",
    version="0.1.1",
    author="Rohit Kosamkar",
    author_email="rohitkosamkar97@gmail.com",
    description="A Python package for seamless SQL Server database management, supporting secure connections, query execution, batch fetching, caching, and result exporting.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rohit180497/PyDBManager",  
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyodbc>=4.0.32",
        "pandas>=1.3.0",
        "python-dotenv>=0.21.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Database :: Database Engines/Servers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="SQL Server, database management, pyodbc, Python, SQL",
    python_requires=">=3.8",
    project_urls={
        "Bug Tracker": "https://github.com/rohit180497/PyDBManager/issues",
        "Documentation": "https://github.com/rohit180497/PyDBManager#readme",
        "Source Code": "https://github.com/rohit180497/PyDBManager"
    },
)

