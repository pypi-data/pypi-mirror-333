# zhanshop-py

#### 介绍
pip install build # 构建工具
pip3 install twine 发布工具

### 创建 pyproject.toml
~~~
[project]
name = "zhanshop"
version = "0.0.1"

~~~

### 创建 setup.cfg
~~~
[metadata]
name = zhanshop
version = 0.0.1

~~~

### 创建 setup.py
~~~
from setuptools import setup

setup(
    name="zhanshop",
    version="0.0.1"
)

~~~

### 使用 .pypirc 文件来存储你的 PyPI 凭据。在你的主目录下创建一个名为 .pypirc 的文件，内容如下

~~~~
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: __token__
password: your_password

[testpypi]
repository: https://test.pypi.org/legacy/
username: __token__
password: your_password
~~~~

## 开始构建
~~~~
#创建分发包，使用 setuptools 创建一个分发包（通常是 .tar.gz 或 .whl 文件）

python setup.py sdist bdist_wheel


#发布
twine upload dist/*

~~~~

