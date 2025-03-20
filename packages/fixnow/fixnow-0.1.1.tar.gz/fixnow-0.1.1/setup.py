from setuptools import setup, find_packages

setup(
    name="fixnow",
    version="0.1.1",  # 🔥 初回リリースバージョン
    packages=find_packages(),
    install_requires=[
        "openai",
        "pre-commit",
        "pylint",
        "mypy",
        "pytest",
        "argparse",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "fixnow=fixnow.fixnow:main",  # 🔥 `fixnow` コマンドを追加！
        ]
    },
    author="Structax",
    author_email="your-email@example.com",
    description="AI-powered Git commit fixer",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Structax/fixnow",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
