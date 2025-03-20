from setuptools import setup, find_packages

setup(
    name="health-report_server_demo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "django",
        "djangorestframework",  # Add other dependencies from requirements.txt
    ],
    entry_points={
        "console_scripts": [
            "health_report=health_report_pkg.cli:main",
        ],
    },
    include_package_data=True,
    description="A Django-based health report system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your@email.com",
    url="https://github.com/yourusername/health_report",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
