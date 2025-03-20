from setuptools import setup, find_packages

setup(
    name="login-canaime",  # Nome de distribuição usado no pip
    version="1.2.0",
    description="Sistema de login Canaimé para gerenciamento de unidades prisionais.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Anderson Assunção",
    author_email="andersongomesrr@hotmail.com",
    url="https://github.com/A-Assuncao/login-canaime_project",
    packages=find_packages(),  # Isso encontrará o pacote "loginCanaime"
    install_requires=[
        "PySide6>=6.0.0",
        "playwright>=1.30.0",
        "qasync>=0.24.0",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "canaime-login=loginCanaime.main:cli_main",
        ],
    },
    include_package_data=True,
    package_data={
        "loginCanaime": ["*.png", "*.ico", "*.ui"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="login, canaime, browser automation, prison management",
)