from setuptools import setup, find_packages

setup(
    name="TestHub",  # Name of your library
    version="0.1.0",  # Initial version number
    author="Dearygt.",
    author_email="test.hub.kys.gay@gmail.com",
    description="Library for interacting with TestHub APIs, ChatGPT, and more.",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/TestHub",  # Repository URL (optional)
    packages=find_packages(),  # Find the packages inside TestHub/
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Or whatever license you use
        "Operating System :: OS Independent",
    ],
    install_requires=[  # Here you can list the dependencies for your library
        "requests>=2.25.1",  # For example, the requests library
    ],
    python_requires=">=3.6",  # You can specify the minimum Python version
)
