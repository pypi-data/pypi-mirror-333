from setuptools import setup, find_packages

setup(
    name="xjtu-enre",  # 替换为你的工具名称（必须唯一）
    version="0.1.0",  # 初始版本号
    author="xjtu",
    author_email="1811765371@qq.com",
    description="supports the extraction of entities and their dependencies from systems written in multiple languages, enables the customization of dependencies of interest to the user, and makes implicit dependencies explicit.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xjtu-enre/ENRE-py.git",  # 你的项目主页链接
    packages=find_packages(),  # 自动发现项目中的包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  # 支持的 Python 版本
    install_requires=[
         "requests>=2.25.1",  # 在这里列出项目依赖
    ],
)