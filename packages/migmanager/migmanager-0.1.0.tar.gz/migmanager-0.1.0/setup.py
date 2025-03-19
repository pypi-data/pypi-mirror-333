from setuptools import setup, find_packages

setup(
    name="migmanager",
    version="0.1.0",
    author="Jitesh Rajpal",
    author_email="jiteshrajpal2508@gmail.com",
    description="A Python package for managing and scheduling jobs on MIG-enabled GPUs dynamically.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JiteshRajpal/migmanager.git",  # Update this with actual repo link
    packages=find_packages(),
    install_requires=[
        "setuptools",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "migmanager-run=migmanager.run_jobs:main",
        ],
    },

)
