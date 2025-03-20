from setuptools import setup,find_packages

setup(
    name="session-conductor-client",
    versio="0.1.0",
    packages=find_packages(),
    install_requires=["requests","schedule"],
    author="Chamindika Kodithuwakku",
    author_email="chamindika1996@gmail.com",
    description="Client library for interacting with the Session Conductor.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chamindika33/session-conductor-client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)