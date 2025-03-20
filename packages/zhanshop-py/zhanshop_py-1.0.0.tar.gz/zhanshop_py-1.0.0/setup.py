from setuptools import setup

setup(
    name="zhanshop_py",
    version="1.0.0",
    author="张启全",
    author_email="admin@zhanshop.cn",
    description="张启全的python框架",
    #项目地址
    #url="",
    python_requires='>=3.10',
    # 模块依赖
    install_requires=[
        'flask',
        'flask_redis',
        'pymysql',
        'pycryptodome',
        'qiniu',
        'apscheduler'
    ],
)