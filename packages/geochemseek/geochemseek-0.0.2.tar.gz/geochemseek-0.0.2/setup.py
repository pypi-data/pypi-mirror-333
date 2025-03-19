from setuptools import setup, find_packages

setup(
    name="geochemseek",
    version="0.0.2",
    description="A python package for geochemical toolkit",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="QingFengMei",
    author_email="qingfengmei@foxmail.com",
    url="https://github.com/QingFengMei/geochemseek",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[  # 添加依赖声明
        'pandas',
        'matplotlib',
        'numpy',
        # 添加您实际使用的其他库
    ],
    include_package_data=True,
)