from setuptools import setup, find_packages

setup(
    name="djaport",
    version="0.1.0",
    description="Django test utility for generating HTML test reports",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Himanshu Pandey",
    author_email="himanshu.dn.pandey@gmail.com",
    url="https://github.com/hp77-creator/djaport",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "django>=2.2",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Unit",
    ],
    license="MIT",
    keywords="django,testing,reports,html,test runner",
)