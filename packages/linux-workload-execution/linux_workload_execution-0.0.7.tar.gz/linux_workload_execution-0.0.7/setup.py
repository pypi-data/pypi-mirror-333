from setuptools import setup, find_packages
setup(
    name="linux_workload_execution",
    version="0.0.7",
    packages=find_packages(),
    install_requires=["gitdb==4.0.12",
                      "GitPython==3.1.44",
                      "pytest==8.3.4",
                      "paramiko==3.5.1",
                      "requests==2.32.3",
                      "setuptools==75.8.0",
                      "zhmccli==1.12.0",
                      "twine==6.1.0",
                      "build==1.2.2",
                      "pipreqs==0.4.13",
                      ],
    entry_points={
        'console_scripts': [
            'entry_point = linux_workload_execution.__main__:main',]
    },
    description="ZHMCCLI lib",
    long_description="It is a Python package designed to take details like, lpar, ipaddress, script directory and script command as the input, and perform below activities",
    author="Girija",
    author_email= "girija.golla@ibm.com",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    license="MIT",
    include_dirs="*",
    include_package_data=True
)