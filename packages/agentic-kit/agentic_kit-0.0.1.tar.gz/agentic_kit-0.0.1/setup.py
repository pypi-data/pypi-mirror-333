from setuptools import setup, find_packages

setup(
    name='agentic-kit',
    version="0.0.1",
    author="manson",
    author_email="manson.li3307@gmail.com",
    description='EDA agent framework based on Langgraph',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',  # 添加开发状态分类器
        'Intended Audience :: Developers',  # 添加目标受众分类器
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.10',
    # todo: update requirements
    install_requires=[
        "langgraph==0.1.19",
        "langchain==0.2.12",
        "langchain-openai==0.1.20",
        "pandas>=2.2.2",
        "grandalf"
    ],
    keywords=['AI', 'LLM', 'Agent'],
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '.csv']
    },
)
