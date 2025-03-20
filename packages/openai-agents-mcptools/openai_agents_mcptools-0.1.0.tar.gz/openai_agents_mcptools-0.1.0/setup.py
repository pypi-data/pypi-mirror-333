from setuptools import setup, find_packages

setup(
    name='openai_agents_mcptools',  # 包名，小写且唯一
    version='0.1.0',  # 版本号，从 0.1.0 开始
    packages=find_packages(),  # 自动查找包目录
    install_requires=[  # 列出依赖包
        'openai-agents',  # 示例依赖，根据实际情况修改
        'mcp',  # 示例依赖
    ],
    author='shadow',
    author_email='389570357@qq.com',
    description='A tool for integrating MCP with OpenAI Agents SDK',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/shadowcz007/openai-agents-mcptool',  # 项目主页（可选）
    classifiers=[  # 包的分类信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 支持的 Python 版本
)