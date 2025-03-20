from setuptools import setup

setup(
    name="blockrand_q_designer",
    version="0.1.0",
    py_modules=["blockrand_q_designer"],
    author="Guido Narduzzi",
    author_email="narduzzi.guido@gmail.com",
    description="A tool for generating block randomized LC-MS queue designs for full factorial experiments.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nar-g/blockrand_q_designer",  # GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Or your chosen license
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",  # add other dependencies as needed
    ],
    python_requires='>=3.6',
)
