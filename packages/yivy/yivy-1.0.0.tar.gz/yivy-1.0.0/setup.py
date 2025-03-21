from setuptools import setup, find_packages

setup(
    name="yivy",
    version="1.0.0",
    description="A simple and powerful GUI library for desktop and mobile.",
    author="YangHoujing",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "kivy>=2.0.0",  # 用于移动端支持
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)