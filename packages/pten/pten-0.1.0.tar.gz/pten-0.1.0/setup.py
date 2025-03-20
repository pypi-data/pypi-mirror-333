from setuptools import setup, find_packages

requires = ["apscheduler", "lunardate", "openai", "pycryptodome"]
test_requirements = [
    "pytest>=3",
    "pytest-mock>=3",
]

setup(
    name="pten",
    version="0.1.0",
    description="A tool to use Wework API quickly and easily",
    author="PENGyong",
    author_email="1203029076@qq.com",
    url="https://github.com/bendell02/pten",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=requires,
    tests_require=test_requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="wework qywx wechat weixin robot app",
)
