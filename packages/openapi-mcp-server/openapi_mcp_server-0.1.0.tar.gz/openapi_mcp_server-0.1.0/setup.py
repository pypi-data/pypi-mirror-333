from setuptools import setup, find_packages

setup(
    name="openapi_mcp_server",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "mcp[cli]>=1.3.0",
        "pydantic>=2.10.6",
        "python-dotenv>=1.0.1",
        "requests>=2.32.3",
    ],
    author="MCP Author",
    author_email="gaddam.rahul@gmail.com",
    description="OpenAPI MCP Server",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rahgadda/openapi_mcp_server",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
