from setuptools import setup, find_packages

setup(
    name="server-report",
    version="0.1.0",
    author="name",
    author_email="your@email.com",
    description="A standalone Django project for health reporting",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/health-report",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=5.1.6",
        "djangorestframework",
        "psycopg2",  # PostgreSQL support
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "health-report-run=health_package.manage:main",
        ],
    },
)
