from setuptools import setup
import tomli

# Read dependencies from pyproject.toml
with open("pyproject.toml", "rb") as f:
    pyproject_data = tomli.load(f)

# Get dependencies from pyproject.toml
dependencies = pyproject_data["project"]["dependencies"]

setup(
    name="openapi-mcp",
    version="0.1.0",
    description="Automatic MCP server generator for OpenAPI applications - converts OpenAPI endpoints to MCP tools for LLM integration",
    author="Tadata Inc.",
    author_email="itay@tadata.com",
    packages=["openapi_mcp"],
    python_requires=">=3.10",
    install_requires=dependencies,
    entry_points={
        "console_scripts": [
            "openapi-mcp=openapi_mcp.cli:app",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords=["openapi", "mcp", "llm", "claude", "ai", "tools", "api", "conversion", "fastapi", "flask", "django"],
    project_urls={
        "Homepage": "https://github.com/tadata-org/openapi-mcp",
        "Documentation": "https://github.com/tadata-org/openapi-mcp#readme",
        "Bug Tracker": "https://github.com/tadata-org/openapi-mcp/issues",
        "PyPI": "https://pypi.org/project/openapi-mcp/",
        "Source Code": "https://github.com/tadata-org/openapi-mcp",
        "Changelog": "https://github.com/tadata-org/openapi-mcp/blob/main/CHANGELOG.md",
    },
)
