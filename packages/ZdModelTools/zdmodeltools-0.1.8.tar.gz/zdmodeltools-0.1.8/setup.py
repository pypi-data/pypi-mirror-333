from setuptools import setup, find_packages

setup(
    name='ZdModelTools',          # 包名（必须唯一）
    version='0.1.8',            # 版本号
    packages=find_packages(),   # 自动发现包
    install_requires=[          # 依赖列表
        'requests>=2.25.1',
        'numpy>=1.19.5',
        'pandas>=1.1.5',
        'datetime>=4.3',
        'matplotlib>=3.4.3',
        'scikit-learn>=0.24.2',
        'toad>=0.0.5'
    ],
    author='ZhiYu Wang',         # 作者名
    author_email='17853133113@163.com',  # 作者邮箱
    description='This package provides tools for data evaluation and model.',  # 简短描述
    long_description=open('README.md').read(),  # 详细描述（从 README.md 读取）
    long_description_content_type='text/markdown',  # 详细描述格式
    url='http://gitlab.baimaodai.cn/wangzhiyu/modelcode',  # 项目主页
    python_requires='>=3.6',    # Python 版本要求
)